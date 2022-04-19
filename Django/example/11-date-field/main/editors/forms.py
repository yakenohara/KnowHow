from unicodedata import name
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from common.utilities import StrChoiceEnum

from .models import Editor

class EditorEditForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = (
            'name',
            'sex',
        )

class EditorCSVForm(forms.Form):
    
    id = forms.IntegerField(
        validators = [
            # note
            # editors/models.py -> class Editor(models.Model): で
            # `id = models.AutoField` と定義している。
            # `AutoField` は `-2147483648 to 2147483647 are safe` とのことなので、この範囲を有効範囲とする
            # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.IntegerField
            MinValueValidator(limit_value = -2147483648, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
            MaxValueValidator(limit_value = 2147483647, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
        ]
    )
    name = forms.CharField(max_length = 255)

    #
    # CSV ファイル内には、タプル定義の2要素目が定義されている。
    # その為、このフィールドの `choices = ~` の定義は `[('男性', 'male'), ('女性', 'female') ...]` のように
    # タプル要素の 1 つめと 2 つめを逆転させた定義が必要なので、
    # common/utilities.py -> `def makeChoiceEnum(primitiveType):` -> `class _ChoiceEnum(primitiveType, enum.Enum):` 内に新たに定義した、
    # `def reversedChoices(cls):` を使ってタプル内要素を逆転させた配列を取得している
    sex = forms.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False)

    #
    # `class EditorCSVForm(forms.Form):` の `.is_valid()` 実行によるバリデーション確認時にコールされる。  
    # `class EditorEditForm(forms.ModelForm):` のように、`def clean(self):` を定義しなくても、
    # バリデーションが行われるが、`sex` フィールドに定義された '男性'/'女性'/'' -> 'male'/'female'/None へ変換するため、  
    # このように定義することでバリデーション機能をオーバーライドできる。  
    def clean(self):

        # Django が提供するデフォルトのバリデーション機能を実行させるため、
        # このように記載する。  
        cleaned_data = super().clean()

        # `sex` フィールドに定義された '男性'/'女性'/'' -> 'male'/'female'/None へ変換する
        cleaned_data['sex'] = dict(self.fields['sex'].choices).get(cleaned_data['sex'], None)
        #
        # note1
        # `sex = forms.ChoiceField(choices = [('男性', 'male'), ('女性', 'female')])` の `choices = ~` に設定したタプル配列を取得するには、
        # `self.fields['sex'].choices` のように記載することで取得できる
        #
        # note2
        # `sex` フィールドは CSV ファイル内で空文字が設定されていた場合、  
        # editors/models.py -> `class Editor(models.Model):` ->  `class Sex(StrChoiceEnum):` の `.reversedChoices()` を
        # 辞書化したディクショナリオブジェクトのプロパティに存在しないプロパティ '' (空文字列) を検索することになる。
        # KeyError を防ぐ為、`.get()` で取得する。  

        # オーバーライドしたバリデーション動作の結果をオブジェクトとして返す
        return cleaned_data
