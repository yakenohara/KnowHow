import enum

def makeChoiceEnum(primitiveType):
    
    class _ChoiceEnum(primitiveType, enum.Enum):
        
        def __new__(cls, var_inDB, var_inUI):
            """ クラスのインスタンス生成 """
            obj = primitiveType.__new__(cls, var_inDB) # 指定されたプリミティブ型でインスタンスを生成
            obj._value_ = var_inDB # .value で値を取得できるように設定
            obj.choice = (var_inDB, var_inUI)
            return obj

        @classmethod
        def choices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(x, y), (a, b), ...] の形式にして返す
            """
            return [element.choice for element in cls]

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
