from django.db import models

# Create your models here.

class Author(models.Model):
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '名前', max_length = 255, unique = True)
    birthday = models.DateField(verbose_name = '生年月日', null = True, blank = True)

    def __str__(self):
        return self.name
