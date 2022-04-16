from django import forms

from .models import Editor

class EditorEditForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = (
            'name',
        )
