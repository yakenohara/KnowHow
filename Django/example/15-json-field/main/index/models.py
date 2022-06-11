from django.db import models

from common.utilities import StrChoiceEnum

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

    class Tags(StrChoiceEnum):

        # 対象読者
        FOR_KIDS = ('for_kids', '幼年漫画')
        FOR_BOYS = ('for_boys', '少年漫画')
        FOR_GIRLS = ('for_girls', '少女漫画')

        # ジャンル
        GENRE_SCHOOL = ('genre_school', '学園')
        GENRE_COMEDY = ('genre_comedy', 'ギャグ')
        GENRE_FANTASY = ('genre_fantasy', 'ファンタジー')

    tags = models.JSONField(verbose_name = 'タグ', null = True, blank = True)

    @property
    def editorsForView(self):
        """
        WebUI 用の編集者リスト文字列を返す
        """
        str_editors = []
        for str_editor in self.editors.all():
            str_editors.append(str_editor.name)
        return ', '.join(str_editors)
