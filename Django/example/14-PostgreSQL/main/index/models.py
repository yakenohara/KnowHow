from django.db import models

from authors.models import Author

from editors.models import Editor
# Create your models here.

class Book(models.Model):
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '著書名', max_length = 255, unique = True)
    author = models.ForeignKey(Author, verbose_name = '著者名', on_delete = models.SET_NULL, null = True, blank = True)
    editors = models.ManyToManyField(Editor, verbose_name = '編集者名', blank = True)
    # note
    # ManyToManyField では、`null = True` は、`python manage.py makemigrations` の実行で  
    # `index.Book.editors: (fields.W340) null has no effect on ManyToManyField.` の警告が出るるので、使用しない。  

    @property
    def editorsForView(self):
        """
        WebUI 用の編集者リスト文字列を返す
        """
        str_editors = []
        for str_editor in self.editors.all():
            str_editors.append(str_editor.name)
        return ', '.join(str_editors)
