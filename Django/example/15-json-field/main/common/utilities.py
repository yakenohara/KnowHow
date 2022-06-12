import csv
import enum
import io
import urllib.parse

from django.db import models

def makeChoiceEnum(primitiveType):
    
    class _ChoiceEnum(primitiveType, enum.Enum):
        
        def __new__(cls, var_inDB, var_inUI):
            """ クラスのインスタンス生成 """
            obj = primitiveType.__new__(cls, var_inDB) # 指定されたプリミティブ型でインスタンスを生成
            obj._value_ = var_inDB # .value で値を取得できるように設定
            obj.choice = (var_inDB, var_inUI)
            obj.reversedChoice = (var_inUI, var_inDB) # `.choice` のタプル内要素逆転版
            return obj

        @classmethod
        def choices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(x, y), (a, b), ...] の形式にして返す
            """
            return [element.choice for element in cls]

        @classmethod
        def reversedChoices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(y, x), (b, a), ...] の形式にして返す
            `def choices(cls):` のタプル内要素逆転版。
            """
            return [element.reversedChoice for element in cls]

    return _ChoiceEnum # インスタンス化せずにクラスそのものを返す

# str と enum.Enum を多重継承したクラス `class _ChoiceEnum(primitiveType, enum.Enum):` の定義
StrChoiceEnum = makeChoiceEnum(str)
"""
以下のように定義して使用する
## 定義方法
```
class Condition(StrChoiceEnum):
    NEW = ('new', '新品')   # <- この宣言時に `def __new__` が呼ばれる。以降同様。
    NOS = ('nos', '新古品') # new old stock
    USED = ('used', '中古')
```
## 使用方法
 - 'new' を取得するには、`Condition.NEW.value` もしくは `Condition.NEW.choice[0]`
 - '新品' を取得するには `Condition.NEW.choice[1]`
 - [('new', '新品'), ('nos', '新古品'), ('used', '中古')] を取得するには、`Condition.choices()`
"""

def makeVerboseNameVsFieldNameDict(obj_model):
    """
    モデルから verbose_name とフィールド名の対応表を作成して返す
    """
    dict_fieldNameVsVerboseName = {}
    for meta_field in obj_model._meta.get_fields():

        # 外部キー参照されているフィールドがある場合は、
        # models.ManyToOneRel フィールドが生成されるので、これは除外する
        if isinstance(meta_field, models.ManyToOneRel):
            continue
        # ManyToManyField で参照されているフィールドがある場合も同様に除外する
        if isinstance(meta_field, models.ManyToManyRel):
            continue

        str_verbose_name = obj_model._meta.get_field(meta_field.name).verbose_name
        dict_fieldNameVsVerboseName[str_verbose_name] = meta_field.name
    
    return dict_fieldNameVsVerboseName

def makeCSVStringFromDict(dict_models, str_columnDefinitions):
    """
    モデルを辞書配列化したものを CSV 文字列化する
    """
    str_csv = ''
    with io.StringIO() as stream:
        writer = csv.writer(stream)
        writer.writerow(str_columnDefinitions)
        for dict_model in dict_models:
            writer.writerow(dict_model.values())

        # BOM 付き UTF-8 文字列を取得
        str_csv = stream.getvalue().encode('utf-8-sig')
    return str_csv

def getOrdinalString(int_number):
    """
    数値を序数詞 (1st, 2nd, 3rd 等) の文字列にして返す
    """
    return str(int_number) + {1: "st", 2: "nd", 3: "rd"}.get((int_number if 10 < int_number < 14 else int_number % 10), "th")

def getQeryStringInURL(dict_params):
    """
    ディクショナリ化されたクエリ文字列 (クエリストリング) を元に戻す
    """
    str_queryStringInURL = ''

    if dict_params: # クエリ文字列が指定されていた場合
        str_queryStrings = []
        for str_key, var_val in dict_params.items():
            str_queryStrings.append(str_key + '=' + urllib.parse.quote(str(var_val)))
        str_queryStringInURL = '?' + '&'.join(str_queryStrings)

    return str_queryStringInURL

def parseCommaSeparatedList(str_toParse):
    """
    ',' 区切りで記載されたリストをパースして配列化する
    ('\' でエスケープされた '\', ',' を考慮する)
    エスケープシーケンスに不正がある場合、第 2 引数にエラー文字位置を返す
    不正がない場合は、第 2 引数に -1 を返す
    """

    if len(str_toParse) == 0:
        return [], -1

    bl_escaped = False
    str_list = []
    int_probeIndex = -1 # 参照文字位置
    int_startIndex = 0
    
    for char_probe in str_toParse:
        
        int_probeIndex += 1

        # 直前の文字が '\' の場合
        if bl_escaped:

            # エスケープされた '\' もしくは ',' の場合
            if char_probe == '\\' or char_probe == ',':
                bl_escaped = False
                continue

            else: # 直前の文字がエスケープ文字 '\' なのに、当該文字が '\' でも ',' でもない場合
                return str_list, int_probeIndex

        # 直前の文字が '\' ではない場合
        else:
            if char_probe == '\\':
                bl_escaped = True
                continue

            elif char_probe == ',':

                # 文字列を切り出してエスケープシーケンスを元に戻して配列に格納
                str_tmp = str_toParse[int_startIndex:int_probeIndex]
                str_tmp = str_tmp.replace('\,',',')
                str_tmp = str_tmp.replace('\\\\','\\')
                str_list.append(str_tmp)

                int_startIndex = int_probeIndex + 1

    # 最後の文字が '\' の場合
    if bl_escaped:
        return str_list, int_probeIndex

    # 文字列を切り出してエスケープシーケンスを元に戻して配列に格納
    str_tmp = str_toParse[int_startIndex:]
    str_tmp = str_tmp.replace('\,',',')
    str_tmp = str_tmp.replace('\\\\','\\')
    str_list.append(str_tmp)

    return str_list, -1

def is_specifiedArray(type, subject):
    """
    指定型の要素のみをもった配列かどうか検査する
    期待される型の配列出ない場合は Exception を raise する
    """
    if not isinstance(subject, list):
        str_msg = f'Type of specified object is {str(type(subject))}.'
        raise Exception(str_msg)
    
    for obj_elem in subject:
        if not isinstance(obj_elem, type):
            str_msg = f'Unexpected type {str(type(obj_elem))} found in {str(subject)}.'
            raise Exception(str_msg)
