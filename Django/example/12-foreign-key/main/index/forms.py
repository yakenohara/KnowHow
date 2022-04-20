from unicodedata import name
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Book

class BookEditForm(forms.ModelForm):
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
    # name = forms.CharField(max_length = 255)

    # sex = forms.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False)

    # def clean(self):

    #     cleaned_data = super().clean()

    #     cleaned_data['sex'] = dict(self.fields['sex'].choices).get(cleaned_data['sex'], None)
        
    #     return cleaned_data
