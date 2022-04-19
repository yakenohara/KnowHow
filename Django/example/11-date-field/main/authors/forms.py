from unicodedata import name
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from common.utilities import StrChoiceEnum

from .models import Author

class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'name',
            'birthday',
        )

class AuthorCSVForm(forms.Form):
    
    id = forms.IntegerField(
        validators = [
            MinValueValidator(limit_value = -2147483648, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
            MaxValueValidator(limit_value = 2147483647, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
        ]
    )
    name = forms.CharField(max_length = 255)
    birthday = forms.DateField(required = False)
