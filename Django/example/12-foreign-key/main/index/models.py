from django.db import models

from authors.models import Author
# Create your models here.

class Book(models.Model):
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '著書名', max_length = 255, unique = True)
    author = models.ForeignKey(Author, verbose_name = '著者名', on_delete = models.SET_NULL, null = True, blank = True)
