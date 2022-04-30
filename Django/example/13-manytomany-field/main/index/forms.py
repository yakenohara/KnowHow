from unicodedata import name
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from authors.models import Author
from common.utilities import parseCommaSeparatedList
from editors.models import Editor

from .models import Book

class BookEditForm(forms.ModelForm):
    
    # https://docs.djangoproject.com/en/4.0/ref/forms/fields/#django.forms.ModelChoiceField
    author = forms.ModelChoiceField(
        label = '著者名',
        required = False,
        queryset = Author.objects.all().order_by('name'), # `name` フィールドでソートしたリストを表示させる
        error_messages = {
            'invalid_choice': 'すでに削除された著者名が選択されています。再度選択してください。'
        }
    )

    # https://docs.djangoproject.com/en/4.0/ref/forms/fields/#django.forms.ModelMultipleChoiceField
    editors = forms.ModelMultipleChoiceField(
        label = '編集者名',
        required = False,
        queryset = Editor.objects.all().order_by('name'),
        error_messages = {
            'invalid_choice': 'すでに削除された編集者名が選択されています。再度選択してください。'
        }
    )

    class Meta:
        model = Book
        fields = (
            'name',
            'author',
            'editors',
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

    editors = forms.CharField(required = False)

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

        str_editorsInCSV = cleaned_data.get('editors')
        if str_editorsInCSV: # 編集者が指定されている場合

            str_editors, int_errIndex = parseCommaSeparatedList(str_editorsInCSV)

            # エスケープシーケンスに不正がある場合
            if -1 < int_errIndex:
                if int_errIndex == (len(str_editorsInCSV) - 1): # 文字列最後に不正がある場合
                    str_errmsg = f'Unknown escape sequence `{str_editorsInCSV[int_errIndex]}` found in `{str_editorsInCSV}`.'
                else:
                    str_errmsg = f'Unknown escape sequence `\{str_editorsInCSV[int_errIndex]}` found in `{str_editorsInCSV}`.'
                raise ValidationError(str_errmsg, code = 'invalid')
            
            obj_editors = []
            for str_editor in str_editors:
                obj_editor = Editor.objects.filter(name = str_editor).first()

                if not obj_editor: # 編集者が存在しない場合
                    str_errmsg = f'Specified editor `{obj_editor}` not found while cleaning ID: {cleaned_data.get("id")}, name: {cleaned_data.get("name")}.'
                    raise ValidationError(str_errmsg, code = 'invalid')

                obj_editors.append(obj_editor)

            cleaned_data['editors'] = obj_editors

        else: # 編集者が指定されていない場合
            cleaned_data['editors'] = []

        return cleaned_data
