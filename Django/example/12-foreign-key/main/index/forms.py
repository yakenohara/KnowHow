from unicodedata import name
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from authors.models import Author

from .models import Book

class BookEditForm(forms.ModelForm):
    
    # https://docs.djangoproject.com/en/4.0/ref/forms/fields/
    author = forms.ModelChoiceField(
        label = '著者名',
        required = False,
        queryset = Author.objects.all().order_by('name'), # `name` フィールドでソートしたリストを表示させる
        error_messages = {
            'invalid_choice': 'すでに削除された著者名が選択されています。再度選択してください。'
        }
    )

    class Meta:
        model = Book
        fields = (
            'name',
            'author',
        )

class BookCSVForm(forms.Form):
    
    id = forms.IntegerField(
        validators = [
            MinValueValidator(limit_value = -2147483648, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
            MaxValueValidator(limit_value = 2147483647, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
        ]
    )
    name = forms.CharField(max_length = 255)

    author = forms.CharField(max_length = 255, required = False)

    def clean(self):

        cleaned_data = super().clean()
        
        str_author = cleaned_data.get('author')
        if str_author: # 著者が指定されている場合
            obj_author = Author.objects.filter(name = str_author).first()

            if not obj_author: # 著者が存在しない場合
                str_errmsg = f'Specified author`{str_author}` not found while cleaning ID: {cleaned_data.get("id")}, name: {cleaned_data.get("name")}.'
                raise ValidationError(str_errmsg, code = 'invalid')

            cleaned_data['author'] = obj_author

        else: # 著者が指定されていない場合
            cleaned_data['author'] = None

        return cleaned_data
