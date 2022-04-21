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
                        Book.objects.update_or_create(
                            id = obj_toImportBook['id'],
                            defaults = {
                                'name': obj_toImportBook['name'],
                                'author': obj_toImportBook['author'],
                            }
                        )
                        
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
    dictionarizer = makeDictFromBooks

class BookUpdateAPIView(TokenAPIViewForUpdate):
    model = Book
    property_keyword = 'books'
    serializer = BookSerializerForUpdate

class BookDeleteAPIView(TokenAPIViewForDeletion):
    model = Book
