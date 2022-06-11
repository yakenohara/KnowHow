from django import forms

class CSVImputForm(forms.Form):
    mode = forms.ChoiceField(choices = [('update', '更新及び追加'), ('replace', '置き換え')])
    file = forms.FileField()
