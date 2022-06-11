from django import forms

from .models import TokenForRESTAPI

class TokenEditForm(forms.ModelForm):

    # モデル定義で `null = True`` とすると、そのフィールドのドロップダウンメニューに `--------` が追加されてしまう。  
    # フォーム上の入力は TokenForRESTAPI.Expiration.choices() のリスト内からいずれかを必須で選択する仕組みにしたいので、  
    # 以下のようにしてオーバーライドして定義する。  
    expiration = forms.ChoiceField(
        label = '設定有効期限',
        choices = TokenForRESTAPI.Expiration.choices(),
        initial = TokenForRESTAPI.Expiration.ONE_MONTH.value,
    )

    class Meta:
        model = TokenForRESTAPI
        fields = (
            'expiration',
        )
