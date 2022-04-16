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
from common.utilities import makeCSVStringFromDict, makeVerboseNameVsFieldNameDict, getOrdinalString

from .models import Editor
from .forms import EditorEditForm, EditorCSVForm

# Create your views here.

# note  
# `__name__` には自身のモジュール名が入る。  
# この場合は `editors.views` という文字列。  
logger = logging.getLogger(__name__)

class EditorCreate(CreateView):
    model = Editor
    form_class = EditorEditForm
    template_name = 'editors/form.html'
    success_url = reverse_lazy('editors:list')

class EditorsList(ListView):
    model = Editor
    template_name = 'editors/list.html'
    success_url = reverse_lazy('editors:list')

class EditorUpdate(UpdateView):
    model = Editor
    form_class = EditorEditForm
    template_name = 'editors/form.html'
    success_url = reverse_lazy('editors:list')

class EditorDelete(DeleteView):
    model = Editor
    success_url = reverse_lazy('editors:list')

def makeDictFromEditors(model_editors):
    """
    編集者リストを辞書配列化する
    """
    dict_editors = []
    for model_edtir in model_editors:
        dict_tmp = model_to_dict(model_edtir)
        dict_tmp['sex'] = dict(Editor.Sex.choices()).get(model_edtir.sex, '')
        dict_editors.append(dict_tmp)
    return dict_editors

@require_safe # https://docs.djangoproject.com/en/4.0/topics/http/decorators/#django.views.decorators.http.require_safe
def export_as_csv(request):
    
    # 
    # 以下の形式のディクショナリを生成
    # ```
    # {
    #     'ID' : 'id',
    #     '名前' : 'name',
    #     '性別' : 'sex',
    # }
    # ```
    dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Editor())

    obj_idSortedEditors = Editor.objects.all().order_by('id')
    dict_editors = makeDictFromEditors(obj_idSortedEditors) # 編集者リストを辞書配列化
    str_csv = makeCSVStringFromDict(dict_editors, dict_verboseNameVsFieldName.keys()) # 辞書配列を CSV 文字列化

    # CSV ファイルにして出力
    obj_response = HttpResponse(str_csv, content_type = 'text/csv; charsert=utf-8-sig')
    obj_response['Content-Disposition'] = 'attachment; filename="editors.csv"'

    return obj_response

@require_POST # https://docs.djangoproject.com/en/4.0/topics/http/decorators/#django.views.decorators.http.require_POST
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
        return redirect('editors:list') # 一覧へ遷移

    obj_toImportEditors = []
    str_fileName = request.FILES['file'].name
    with io.TextIOWrapper(request.FILES['file'], encoding = 'utf-8-sig') as stream:

        obj_reader = csv.DictReader(stream)

        try:
            str_verboseNamesInProbe = obj_reader.fieldnames
        except UnicodeDecodeError as err:
            # e.g. ファイルの文字コードが SJIS で保存されていた場合
            logger.warning(f'`UnicodeDecodeError` has occured while opening "{str_fileName}". Reason: "{err.reason}"')
            return redirect('editors:list') # 一覧へ遷移

        dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Editor())
        str_requiredHeaders = dict_verboseNameVsFieldName.keys()

        # 必要なカラムタイトルが存在するかどうかチェック
        for str_requiredHeader in str_requiredHeaders:
            if str_requiredHeader not in str_verboseNamesInProbe:
                logger.warning(f'Required header `{str_requiredHeader}` is not defined in "{str_fileName}"')
                return redirect('editors:list') # 一覧へ遷移

        for dict_readRow in obj_reader:
            
            # 必要なプロパティ定義だけをもったディクショナリを生成
            dict_subject = {dict_verboseNameVsFieldName[str_verboseName]: dict_readRow[str_verboseName] for str_verboseName in dict_verboseNameVsFieldName.keys()}

            obj_subjectEditor = EditorCSVForm(dict_subject)

            if obj_subjectEditor.is_valid(): # バリデーション OK の場合
                obj_toImportEditors.append(obj_subjectEditor.cleaned_data)  

            else: # バリデーションエラーの場合
                str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in dict_readRow.items()])
                logger.warning(f'Validation error has occured while loading {str_tmp}. Check following.')
                for str_key, str_errmsgs in obj_subjectEditor.errors.items():
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
                dict_notUpdatedIDs = {obj_editors.id: obj_editors.id for obj_editors in Editor.objects.all()}

                for obj_toImportEditor in obj_toImportEditors:

                    try:
                        Editor.objects.update_or_create(
                            id = obj_toImportEditor['id'],
                            defaults = {
                                'name': obj_toImportEditor['name'],
                                'sex': obj_toImportEditor['sex'],
                            }
                        )
                        
                        # レコードを更新したのでリストから ID を削除
                        dict_notUpdatedIDs.pop(obj_toImportEditor['id'], None)

                    except IntegrityError as err: # `名前` フィールドが他レコードと重複した場合
                        str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in obj_toImportEditor.items()])
                        logger.warning(f'`IntegrityError` has occured while saving {str_tmp}. Check following.')
                        logger.warning(err)
                
                # `置き換え` モードの場合
                if obj_csvImportForm.cleaned_data.get('mode') == 'replace':
                    for int_notUpdatedID in dict_notUpdatedIDs.values():
                        Editor.objects.filter(id = int_notUpdatedID).first().delete()


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
    
    return redirect('editors:list')
