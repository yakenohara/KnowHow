import logging

from asyncio.log import logger
from unicodedata import name
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator

from authors.models import Author

from common.utilities import StrChoiceEnum

from .models import Book

logger = logging.getLogger(__name__)

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'name',
            'author',
        )
    
    def clean_author(self):
        obj_author = None
        str_authorName = self.cleaned_data.get('author')
        if str_authorName:
            try:
                obj_author = Author.objects.get(name = str_authorName)
            except ObjectDoesNotExist as err:
                logger.warning(f'Specified author name `{obj_author}` not found.')
                raise forms.ValidationError('削除済みの著者が選択されました。選択し直してください。')

        return obj_author
    

class BookCSVForm(forms.Form):
    
    id = forms.IntegerField(
        validators = [
            MinValueValidator(limit_value = -2147483648, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
            MaxValueValidator(limit_value = 2147483647, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
        ]
    )
    # name = forms.CharField(max_length = 255)

    # sex = forms.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False)

    # def clean(self):

    #     cleaned_data = super().clean()

    #     cleaned_data['sex'] = dict(self.fields['sex'].choices).get(cleaned_data['sex'], None)
        
    #     return cleaned_data
