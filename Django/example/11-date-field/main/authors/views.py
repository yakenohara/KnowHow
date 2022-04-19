import csv
import io
import logging
import time

from django.db import transaction
from django.db.utils import OperationalError, IntegrityError
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_safe, require_POST
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from common.const import FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK, INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK
from common.forms import CSVImputForm
from common.utilities import makeCSVStringFromDict, makeVerboseNameVsFieldNameDict, getOrdinalString, getQeryStringInURL
from common.views import TokenAPIViewForCreation, TokenAPIViewForList, TokenAPIViewForUpdate, TokenAPIViewForDeletion

from .models import Author
from .forms import AuthorEditForm, AuthorCSVForm
from .serializer import AuthorSerializerForQueryString, AuthorSerializerForCreate, AuthorSerializerForUpdate

# Create your views here.

logger = logging.getLogger(__name__)

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'authors/form.html'
    success_url = reverse_lazy('authors:list')

class AuthorsList(ListView):
    model = Author
    template_name = 'authors/list.html'
    success_url = reverse_lazy('authors:list')

class AuthorUpdate(UpdateView):
    model = Author
    form_class = AuthorEditForm
    template_name = 'authors/form.html'
    success_url = reverse_lazy('authors:list')

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors:list')

def makeDictFromAuthors(cls, model_authors):
    """
    著者リストを辞書配列化する
    """
    dict_authors = []
    for model_edtir in model_authors:
        dict_tmp = model_to_dict(model_edtir)
        dict_authors.append(dict_tmp)
    return dict_authors

@require_safe
def export_as_csv(request):
    
    # 
    # 以下の形式のディクショナリを生成
    # ```
    # {
    #     'ID' : 'id',
    #     '名前' : 'name',
    #     '生年月日' : 'birthday',
    # }
    # ```
    dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Author())

    obj_idSortedAuthors = Author.objects.all().order_by('id')
    dict_authors = makeDictFromAuthors(None, obj_idSortedAuthors) # 編集者リストを辞書配列化
    str_csv = makeCSVStringFromDict(dict_authors, dict_verboseNameVsFieldName.keys()) # 辞書配列を CSV 文字列化

    # CSV ファイルにして出力
    obj_response = HttpResponse(str_csv, content_type = 'text/csv; charsert=utf-8-sig')
    obj_response['Content-Disposition'] = 'attachment; filename="authors.csv"'

    return obj_response

@require_POST
def import_from_csv(request):
    
    obj_csvImportForm = CSVImputForm(request.POST, request.FILES)

    #
    # インスタンス化したフォームクラスの `.is_valid()` をコールすることで、  
    # バリデーションを確認することができる。  
    # ここでは、CSVImputForm のバリデーションエラーとなっていないかどうかを確認している。
    # 以下のようなパターンの場合に、バリデーションエラーとなる。  
    # e.g.
    #  - `mode` フィールドが存在しない
    #  - `mode` フィールドの値が `update` でも `replace` でもない
    #  - ファイルが指定されていない
    if not obj_csvImportForm.is_valid():
        for str_key, str_errmsgs in obj_csvImportForm.errors.items():
            logger.warning(f'{str_key}: "{str_errmsgs[0]}"')
        return redirect('authors:list') # 一覧へ遷移

    obj_toImportAuthors = []
    str_fileName = request.FILES['file'].name
    with io.TextIOWrapper(request.FILES['file'], encoding = 'utf-8-sig') as stream:

        obj_reader = csv.DictReader(stream)

        try:
            str_verboseNamesInProbe = obj_reader.fieldnames
        except UnicodeDecodeError as err:
            # e.g. ファイルの文字コードが SJIS で保存されていた場合
            logger.warning(f'`UnicodeDecodeError` has occured while opening "{str_fileName}". Reason: "{err.reason}"')
            return redirect('authors:list') # 一覧へ遷移

        dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Author())
        str_requiredHeaders = dict_verboseNameVsFieldName.keys()

        # 必要なカラムタイトルが存在するかどうかチェック
        for str_requiredHeader in str_requiredHeaders:
            if str_requiredHeader not in str_verboseNamesInProbe:
                logger.warning(f'Required header `{str_requiredHeader}` is not defined in "{str_fileName}"')
                return redirect('authors:list') # 一覧へ遷移

        for dict_readRow in obj_reader:
            
            # 必要なプロパティ定義だけをもったディクショナリを生成
            dict_subject = {dict_verboseNameVsFieldName[str_verboseName]: dict_readRow[str_verboseName] for str_verboseName in dict_verboseNameVsFieldName.keys()}

            obj_subjectAuthor = AuthorCSVForm(dict_subject)

            if obj_subjectAuthor.is_valid(): # バリデーション OK の場合
                obj_toImportAuthors.append(obj_subjectAuthor.cleaned_data)  

            else: # バリデーションエラーの場合
                str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in dict_readRow.items()])
                logger.warning(f'Validation error has occured while loading {str_tmp}. Check following.')
                for str_key, str_errmsgs in obj_subjectAuthor.errors.items():
                    logger.warning(f'{str_key}: "{str_errmsgs[0]}"')

    #
    # トランザクション試行ループ。  
    # 複数ユーザーから同時にこの機能が実行されると、DB のデッドロックが発生する可能性があるため、  
    # SQL 文が発行されるコードは以下の `with transaction.atomic():` 内で記述し、  
    # デッドロックが発生した場合は `OperationalError` が発生するのでそれをキャッチ。  
    # 一定時間スリープしてリトライする。  
    bl_retrying = True
    int_tryTime = 1
    while bl_retrying:
        try:
            with transaction.atomic():
                # この with 文内で実行される SQL 文はまとめて実行される。

                # 全ての ID リストをここで取得し、レコードを更新する度にこのリストから ID を削除していく。
                dict_notUpdatedIDs = {obj_editors.id: obj_editors.id for obj_editors in Author.objects.all()}

                for obj_toImportAuthor in obj_toImportAuthors:

                    try:
                        Author.objects.update_or_create(
                            id = obj_toImportAuthor['id'],
                            defaults = {
                                'name': obj_toImportAuthor['name'],
                                'birthday': obj_toImportAuthor['birthday'],
                            }
                        )
                        
                        # レコードを更新したのでリストから ID を削除
                        dict_notUpdatedIDs.pop(obj_toImportAuthor['id'], None)

                    except IntegrityError as err: # `名前` フィールドが他レコードと重複した場合
                        str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in obj_toImportAuthor.items()])
                        logger.warning(f'`IntegrityError` has occured while saving {str_tmp}. Check following.')
                        logger.warning(err)
                
                # `置き換え` モードの場合
                if obj_csvImportForm.cleaned_data.get('mode') == 'replace':
                    for int_notUpdatedID in dict_notUpdatedIDs.values():
                        Author.objects.filter(id = int_notUpdatedID).first().delete()


        except OperationalError as err:
            # デッドロックの可能性。既定回数分リトライする。
            
            logger.warning(f'There is a possibility of deadlock. This is the {getOrdinalString(int_tryTime)} time attempt. Check following.')
            logger.warning(str(err))

            if int_tryTime < INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK: # 既定回数以内の場合
                # スリープして再試行
                time.sleep(FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK)
                int_tryTime += 1
                logger.warning('Transaction retrying...')
                continue

            else:
                logger.error(f'The number of record saving attempts has reached the upper limit ({INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK} times).')
        
        # `OperationalError` が発生しなかった場合または `OperationalError` が規定回数繰り返し発生した場合
        bl_retrying = False
    
    return redirect('authors:list')

class AuthorCreateAPIView(TokenAPIViewForCreation):
    property_keyword = 'authors'
    serializer = AuthorSerializerForCreate

class AuthorListAPIView(TokenAPIViewForList):
    model = Author
    property_keyword = 'authors'
    serializer = AuthorSerializerForQueryString
    dictionarizer = makeDictFromAuthors

class AuthorUpdateAPIView(TokenAPIViewForUpdate):
    model = Author
    property_keyword = 'authors'
    serializer = AuthorSerializerForUpdate

class AuthorDeleteAPIView(TokenAPIViewForDeletion):
    model = Author


from rest_framework import status, serializers

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_serializer, OpenApiParameter, OpenApiResponse, OpenApiExample
# https://drf-spectacular.readthedocs.io/en/latest/drf_spectacular.html?highlight=openapiviewextension#drf_spectacular.extensions.OpenApiViewExtension
# https://drf-spectacular.readthedocs.io/en/latest/blueprints.html?highlight=Fixed#dj-stripe

from common.views import InvalidReasonSerializerForDoc

class AuthorCreationSerializerForDoc(serializers.Serializer):
    name = serializers.CharField(help_text = '名前を指定します。他の著者と同じの名前は登録できません。また、空文字も無効です。')
    birthday = serializers.CharField(help_text = '任意で生年月日を指定します。', required = False)

class AuthorCreationArraySerializerForDoc(serializers.Serializer):
    class AuthorCreationSerializer(AuthorCreationSerializerForDoc):
        pass
    editors = AuthorCreationSerializer(many = True)

class AuthorCreateOpenApiView(OpenApiViewExtension):

    target_class = AuthorCreateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著者管理'],
                operation_id = '著者の追加',
                description = '著者を追加します。',
                request = AuthorCreationArraySerializerForDoc,
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'JSON ファイルのパースエラーもしくはバリデーションエラー'
                    ),
                    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '`OperationalError` の発生。デッドロックの可能性。'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '誕生日指定',
                        description = '誕生日指定',
                        request_only = True,
                        value = {
                            "authors" : [
                                {
                                    "name" : "author A",
                                    "birthday" : "2003-07-18"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '誕生日未指定 (null)',
                        description = '誕生日未指定 (null)',
                        request_only = True,
                        value = {
                            "authors" : [
                                {
                                    "name" : "author A",
                                    "birthday" : null
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別未指定 (プロパティなし)',
                        description = '性別未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "authors" : [
                                {
                                    "name" : "Foo Bar"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = 'パースエラー (400 NG)',
                        description = 'JSON ファイルのパースエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 72 (char 71)\nrequest.body: b'{  \"authors\": [    {      \"name\": \"null\",      \"birthday\": null    }  ]'"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Author が既に存在します。', code='invalid')]}"
                        },
                    ),
                    OpenApiExample(
                        name = 'OperationalError (500 NG)',
                        description = 'デッドロックの可能性 (500 NG)',
                        status_codes = [str(status.HTTP_500_INTERNAL_SERVER_ERROR)],
                        response_only = True,
                        value = {
                            "detail": "database is locked"
                        },
                    ),
                ],
            )

            def post(self, request, *args, **kwargs):
                pass

        return Fixed

class AuthorListSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID')
    name = serializers.CharField(help_text = '名前')
    birthday = serializers.DateField(help_text = '生年月日')

class AuthorListupedArraySerializerForDoc(serializers.Serializer):
    class AuthorListSerializer(AuthorListSerializerForDoc):
        pass
    editors = AuthorListSerializer(many = True)

class AuthorListOpenApiView(OpenApiViewExtension):
    
    target_class = AuthorListAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著者管理'],
                operation_id = '著者一覧の取得',
                description = '著者の一覧を取得します。',
                parameters = [
                    OpenApiParameter(name = 'id', description = 'ID', required = False, type = int),
                    OpenApiParameter(name = 'name', description = '名前', required = False, type = str),
                ],
                responses = {
                    status.HTTP_200_OK: OpenApiResponse(
                        response = AuthorListupedArraySerializerForDoc,
                        description = '著者の一覧'
                    ),
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'クエリ文字列 (クエリストリング) のパースエラー'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '200 OK',
                        description = '取得例 (200 OK)',
                        status_codes = [str(status.HTTP_200_OK)],
                        value = {
                            "authors": [
                                {
                                    "id": 1,
                                    "name": "author A",
                                    "birthday": null
                                },
                                {
                                    "id": 2,
                                    "name": "author B",
                                    "birthday": "2022-04-19"
                                }
                            ]
                        },
                    ),
                    OpenApiExample(
                        name = '400 NG',
                        description = '取得例 (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        value = {
                            "detail": "Validation error found in /api/v1/authors.json/?id=a"
                        },
                    ),
                ],
            )

            def get(self, request, *args, **kwargs):
                pass

        return Fixed

class AuthorUpdateSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID を指定します。存在しない ID は指定できません。')
    name = serializers.CharField(help_text = '名前を指定します。他の編集者と同じの名前は指定できません。また、空文字も無効です。')
    birthday = serializers.DateField(help_text = '任意で生年月日を指定します。', required = False)

class AuthorUpdatingArraySerializerForDoc(serializers.Serializer):
    class AuthorUpdateSerializer(AuthorUpdateSerializerForDoc):
        pass
    editors = AuthorUpdateSerializer(many = True)

class AuthorUpdateOpenApiView(OpenApiViewExtension):
    
    target_class = AuthorUpdateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著者管理'],
                operation_id = '著者の編集',
                description = '著者の情報を更新します。',
                request = AuthorUpdatingArraySerializerForDoc,
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'JSON ファイルのパースエラーもしくはバリデーションエラー'
                    ),
                    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '`OperationalError` の発生。デッドロックの可能性。'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '生年月日指定',
                        description = '生年月日指定',
                        request_only = True,
                        value = {
                            "authors": [
                                {
                                    "id" : 1,
                                    "name" : "author A",
                                    "birthday" : "2000-06-10"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '生年月日未指定 (null)',
                        description = '生年月日未指定 (null)',
                        request_only = True,
                        value = {
                            "authors": [
                                {
                                    "id" : 1,
                                    "name" : "author A",
                                    "birthday" : null
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '生年月日未指定 (プロパティなし)',
                        description = '生年月日未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "authors": [
                                {
                                    "id" : 1,
                                    "name" : "author A"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = 'パースエラー (400 NG)',
                        description = 'JSON ファイルのパースエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 98 (char 97)\nrequest.body: b'{  \"authors\": [    {      \"id\": 1,      \"name\": \"author A\",      \"birthday\": \"2000-06-10\"    }  ]'"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Author が既に存在します。', code='invalid')]}"
                        },
                    ),
                    OpenApiExample(
                        name = 'OperationalError (500 NG)',
                        description = 'デッドロックの可能性 (500 NG)',
                        status_codes = [str(status.HTTP_500_INTERNAL_SERVER_ERROR)],
                        response_only = True,
                        value = {
                            "detail": "database is locked"
                        },
                    ),
                ]
            )

            def post(self, request, *args, **kwargs):
                pass

        return Fixed


class EditorDeleteOpenApiView(OpenApiViewExtension):
    
    target_class = AuthorDeleteAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            @extend_schema(
                tags = ['著者管理'],
                operation_id = '著者の削除',
                description = '指定 ID の著者を削除します。',
                parameters = [
                    OpenApiParameter(name = 'id', description = 'ID', location = OpenApiParameter.PATH , type = int),
                ],
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_404_NOT_FOUND: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '指定 ID が存在しないエラー'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '指定 ID 検索エラー (404 NG)',
                        description = '指定 ID が存在しないエラー (404 NG)',
                        status_codes = [str(status.HTTP_404_NOT_FOUND)],
                        value = {
                            "detail": "Specified Author ID: 1 not found."
                        },
                    ),
                ]
            )

            def delete(self, request, pk, *args, **kwargs):
                pass

        return Fixed
