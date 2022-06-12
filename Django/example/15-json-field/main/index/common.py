from .models import Book

def convertUIValToInternalVal(str_uiVals):
    """
    タグを表す配列の内部的な変数の表記方法を WebUI で使用される文字列の表記方法に変換して返す
    存在しない WebUI 表記の文字列が指定された場合は、KeyError を返す
    e.g.
    ['幼年漫画', '学園'] -> ['for_kids', 'genre_school']
    """
    str_internalVals = []
    dict_UIValVSInternalVal = dict(Book.Tags.reversedChoices())
    for str_uiVal in str_uiVals:
        str_internalVal = dict_UIValVSInternalVal.get(str_uiVal, None)
        if str_internalVal: # 指定 WebUI 文字列が存在する場合
            str_internalVals.append(str_internalVal)
        else: # 指定 WebUI 文字列が存在しない場合
            str_errmsg = f'Specified `{str_uiVal}` WebUI string not found in Book.Tags'
            raise KeyError(str_errmsg)
    return str_internalVals
