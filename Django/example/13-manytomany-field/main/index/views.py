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
from django.views.generic import TemplateView
from authors.models import Author

from common.const import FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK, INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK
from common.forms import CSVImputForm
from common.utilities import makeCSVStringFromDict, makeVerboseNameVsFieldNameDict, getOrdinalString, getQeryStringInURL
from common.views import TokenAPIViewForCreation, TokenAPIViewForList, TokenAPIViewForUpdate, TokenAPIViewForDeletion
from editors.models import Editor

from .forms import BookEditForm, BookCSVForm
from .models import Book
from .serializer import BookSerializerForCreate, BookSerializerForQueryString, BookSerializerForUpdate

# Create your views here.

logger = logging.getLogger(__name__)

class BookCreate(CreateView):
    model = Book
    form_class = BookEditForm
    template_name = 'index/form.html'
    success_url = reverse_lazy('index:index')

class Index(ListView):
    model = Book
    template_name = 'index/index.html'
    success_url = reverse_lazy('index:index')

class BookUpdate(UpdateView):
    model = Book
    form_class = BookEditForm
    template_name = 'index/form.html'
    success_url = reverse_lazy('index:index')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('index:index')

def makeDictFromBooks(cls, model_books):
    """
    書籍リストを辞書配列化する
    """
    dict_books = []
    for model_book in model_books:
        dict_tmp = model_to_dict(model_book)
        int_author = dict_tmp.get('author', None)
        if int_author: # 著者が指定されている場合
            dict_tmp['author'] = Author.objects.get(id = int_author).name
        else: # 著者が指定されていない場合
            dict_tmp['author'] = ''
        obj_editors = dict_tmp.get('editors', None)
        if obj_editors: # 編集者が指定されている場合
            str_editors = []
            for tmp_editor in obj_editors:
                tmp_str = tmp_editor.name.replace('\\','\\\\') # 著者名に ',' が含まれている場合は '\' でエスケープ
                tmp_str = tmp_str.replace(',','\,') # 著者名に '\' が含まれている場合は '\' でエスケープ
                str_editors.append(tmp_str)
            dict_tmp['editors'] = ','.join(str_editors)
        else: # 著者が指定されていない場合
            dict_tmp['editors'] = ''
        dict_books.append(dict_tmp)
    return dict_books

def makeDictFromBooksForRESTAPI(cls, model_books):
    """
    書籍リストを辞書配列化する
    """
    dict_books = []
    for model_book in model_books:
        dict_tmp = model_to_dict(model_book)
        int_author = dict_tmp.get('author', None)
        if int_author: # 著者が指定されている場合
            dict_tmp['author'] = Author.objects.get(id = int_author).name
        else: # 著者が指定されていない場合
            dict_tmp['author'] = ''
        obj_editors = dict_tmp.get('editors', None)
        str_editors = []
        if obj_editors: # 編集者が指定されている場合
            for tmp_editor in obj_editors:
                str_editors.append(tmp_editor.name)
            dict_tmp['editors'] = ','.join(str_editors)
        dict_tmp['editors'] = str_editors
        dict_books.append(dict_tmp)
    return dict_books

@require_safe
def export_as_csv(request):
    
    # 
    # 以下の形式のディクショナリを生成
    # ```
    # {
    #     'ID' : 'id',
    #     '名前' : 'name',
    #     '著者' : 'author',
    # }
    # ```
    dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Book())

    obj_idSortedBooks = Book.objects.all().order_by('id')
    dict_books = makeDictFromBooks(None, obj_idSortedBooks) # 書籍リストを辞書配列化
    str_csv = makeCSVStringFromDict(dict_books, dict_verboseNameVsFieldName.keys()) # 辞書配列を CSV 文字列化

    # CSV ファイルにして出力
    obj_response = HttpResponse(str_csv, content_type = 'text/csv; charsert=utf-8-sig')
    obj_response['Content-Disposition'] = 'attachment; filename="books.csv"'

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
        return redirect('index:index') # 一覧へ遷移

    obj_toImportBooks = []
    str_fileName = request.FILES['file'].name
    with io.TextIOWrapper(request.FILES['file'], encoding = 'utf-8-sig') as stream:

        obj_reader = csv.DictReader(stream)

        try:
            str_verboseNamesInProbe = obj_reader.fieldnames
        except UnicodeDecodeError as err:
            # e.g. ファイルの文字コードが SJIS で保存されていた場合
            logger.warning(f'`UnicodeDecodeError` has occured while opening "{str_fileName}". Reason: "{err.reason}"')
            return redirect('index:index') # 一覧へ遷移

        dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Book())
        str_requiredHeaders = dict_verboseNameVsFieldName.keys()

        # 必要なカラムタイトルが存在するかどうかチェック
        for str_requiredHeader in str_requiredHeaders:
            if str_requiredHeader not in str_verboseNamesInProbe:
                logger.warning(f'Required header `{str_requiredHeader}` is not defined in "{str_fileName}"')
                return redirect('index:index') # 一覧へ遷移

        for dict_readRow in obj_reader:
            
            # 必要なプロパティ定義だけをもったディクショナリを生成
            dict_subject = {dict_verboseNameVsFieldName[str_verboseName]: dict_readRow[str_verboseName] for str_verboseName in dict_verboseNameVsFieldName.keys()}

            obj_subjectBook = BookCSVForm(dict_subject)

            if obj_subjectBook.is_valid(): # バリデーション OK の場合
                obj_toImportBooks.append(obj_subjectBook.cleaned_data)  

            else: # バリデーションエラーの場合
                str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in dict_readRow.items()])
                logger.warning(f'Validation error has occured while loading {str_tmp}. Check following.')
                for str_key, str_errmsgs in obj_subjectBook.errors.items():
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
                dict_notUpdatedIDs = {obj_books.id: obj_books.id for obj_books in Book.objects.all()}

                for obj_toImportBook in obj_toImportBooks:

                    try:
                        obj_book, _ = Book.objects.update_or_create(
                            id = obj_toImportBook['id'],
                            defaults = {
                                'name': obj_toImportBook['name'],
                                'author': obj_toImportBook['author'],
                            }
                        )

                        # ManyToManyField は `update_or_create` 内でセットできない為、ここで個別にセットする
                        if obj_toImportBook['editors']:
                            obj_book.editors.set(obj_toImportBook['editors'])
                            obj_book.save()

                        # レコードを更新したのでリストから ID を削除
                        dict_notUpdatedIDs.pop(obj_toImportBook['id'], None)

                    except IntegrityError as err: # `著書名` フィールドが他レコードと重複した場合
                        str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in obj_toImportBook.items()])
                        logger.warning(f'`IntegrityError` has occured while saving {str_tmp}. Check following.')
                        logger.warning(err)
                
                # `置き換え` モードの場合
                if obj_csvImportForm.cleaned_data.get('mode') == 'replace':
                    for int_notUpdatedID in dict_notUpdatedIDs.values():
                        Book.objects.filter(id = int_notUpdatedID).first().delete()


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
    
    return redirect('index:index')

class BookCreateAPIView(TokenAPIViewForCreation):
    property_keyword = 'books'
    serializer = BookSerializerForCreate

class BookListAPIView(TokenAPIViewForList):
    model = Book
    property_keyword = 'books'
    serializer = BookSerializerForQueryString
    dictionarizer = makeDictFromBooksForRESTAPI

class BookUpdateAPIView(TokenAPIViewForUpdate):
    model = Book
    property_keyword = 'books'
    serializer = BookSerializerForUpdate

class BookDeleteAPIView(TokenAPIViewForDeletion):
    model = Book


from rest_framework import status, serializers

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from common.views import InvalidReasonSerializerForDoc

from index.serializer import WordListingField

class BookCreationSerializerForDoc(serializers.Serializer):
    name = serializers.CharField(help_text = '名前を指定します。他の著書と同じの名前は登録できません。また、空文字も無効です。')
    author = serializers.CharField(help_text = '任意で著者名を指定します。存在しない著者名は登録できません', required = False)
    editors = WordListingField(help_text = '任意で編集者名を指定します。存在しない編集者名は登録できません', many = True, required = False)

class BookCreationArraySerializerForDoc(serializers.Serializer):
    class BookCreationSerializer(BookCreationSerializerForDoc):
        pass
    editors = BookCreationSerializer(many = True)

class BookCreateOpenApiView(OpenApiViewExtension):

    target_class = BookCreateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著書管理'],
                operation_id = '著書の追加',
                description = '著書を追加します。',
                request = BookCreationArraySerializerForDoc,
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
                        name = '著者名指定',
                        description = '著者名指定',
                        request_only = True,
                        value = {
                            "books" : [
                                {
                                    "name" : "book A",
                                    "author" : "author A"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '著者名未指定(空文字)',
                        description = '著者名未指定(空文字)',
                        request_only = True,
                        value = {
                            "books" : [
                                {
                                    "name" : "book A",
                                    "author" : ""
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '編集者名指定',
                        description = '編集者名指定',
                        request_only = True,
                        value = {
                            "books" : [
                                {
                                    "name" : "book A",
                                    "editors" : [
                                        "Editor A",
                                        "Editor B"
                                    ]
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '編集者名未指定(空配列)',
                        description = '編集者名未指定(空配列)',
                        request_only = True,
                        value = {
                            "books" : [
                                {
                                    "name" : "book A",
                                    "editors" : []
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '著者名・編集者未指定 (プロパティなし)',
                        description = '著者名・編集者未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "books" : [
                                {
                                    "name" : "book A"
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
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 90 (char 89)\nrequest.body: b'{    \"books\": [      {        \"name\": \"book A\",        \"author\": \"author A\"      }    ]  '"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Book が既に存在します。', code='invalid')]}"
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

class BookListSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID')
    name = serializers.CharField(help_text = '著書名')
    author = serializers.DateField(help_text = '著者名')
    editors = WordListingField(help_text = '編集者名', many = True)

class BookListupedArraySerializerForDoc(serializers.Serializer):
    class BookListSerializer(BookListSerializerForDoc):
        pass
    books = BookListSerializer(many = True)

class AuthorListOpenApiView(OpenApiViewExtension):
    
    target_class = BookListAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著書管理'],
                operation_id = '著書一覧の取得',
                description = '著書の一覧を取得します。',
                parameters = [
                    OpenApiParameter(name = 'id', description = 'ID', required = False, type = int),
                    OpenApiParameter(name = 'name', description = '著書名', required = False, type = str),
                ],
                responses = {
                    status.HTTP_200_OK: OpenApiResponse(
                        response = BookListupedArraySerializerForDoc,
                        description = '著書の一覧'
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
                            "books": [
                                {
                                    "id": 1,
                                    "name": "book A",
                                    "author": "author A",
                                    "editors": [
                                        "editor A",
                                        "editor B"
                                    ]
                                },
                                {
                                    "id": 2,
                                    "name": "book B",
                                    "author": "",
                                    "editors": []
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '400 NG',
                        description = '取得例 (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        value = {
                            "detail": "Validation error found in /api/v1/books.json/?id=a"
                        },
                    ),
                ],
            )

            def get(self, request, *args, **kwargs):
                pass

        return Fixed

class BookUpdateSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID を指定します。存在しない ID は指定できません。')
    name = serializers.CharField(help_text = '著書名を指定します。他の著書名と同じの名前は指定できません。また、空文字も無効です。')
    author = serializers.CharField(help_text = '任意で著者名を指定します。存在しない著者名は登録できません', required = False)
    editors = WordListingField(help_text = '任意で編集者名を指定します。存在しない 編集者名は登録できません', many = True, required = False)

class BookUpdatingArraySerializerForDoc(serializers.Serializer):
    class BookUpdateSerializer(BookUpdateSerializerForDoc):
        pass
    editors = BookUpdateSerializer(many = True)

class AuthorUpdateOpenApiView(OpenApiViewExtension):
    
    target_class = BookUpdateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            null = None
            
            @extend_schema(
                tags = ['著書管理'],
                operation_id = '著書の編集',
                description = '著書の情報を更新します。',
                request = BookUpdatingArraySerializerForDoc,
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
                        name = '著者名指定',
                        description = '著者名指定',
                        request_only = True,
                        value = {
                            "books": [
                                {
                                    "id" : 1,
                                    "name" : "book A",
                                    "author" : "author A"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '編集者名指定',
                        description = '編集者名指定',
                        request_only = True,
                        value = {
                            "books": [
                                {
                                    "id" : 1,
                                    "name" : "book A",
                                    "editors" : [
                                        "editor A",
                                        "editor B"
                                    ]
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '著者名未指定 (空文字)',
                        description = '著者名未指定 (空文字)',
                        request_only = True,
                        value = {
                            "books": [
                                {
                                    "id" : 1,
                                    "name" : "book A",
                                    "author" : ""
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '編集者名未指定 (空配列)',
                        description = '編集者名未指定 (空配列)',
                        request_only = True,
                        value = {
                            "books": [
                                {
                                    "id" : 1,
                                    "name" : "book A",
                                    "editors" : []
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '著者名・編集者名未指定 (プロパティなし)',
                        description = '著者名・編集者名未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "books": [
                                {
                                    "id" : 1,
                                    "name" : "book A"
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
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 106 (char 105)\nrequest.body: b'{    \"books\": [      {        \"id\": 1,        \"name\": \"book A\",        \"author\": \"author A\"      }    ]  '"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Book が既に存在します。', code='invalid')]}"
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

class BookDeleteOpenApiView(OpenApiViewExtension):
    
    target_class = BookDeleteAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            @extend_schema(
                tags = ['著書管理'],
                operation_id = '著書の削除',
                description = '指定 ID の著書を削除します。',
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
                            "detail": "Specified Book ID: 1 not found."
                        },
                    ),
                ]
            )

            def delete(self, request, pk, *args, **kwargs):
                pass

        return Fixed
