from django.db import models

# Create your models here.

# note
# ここに定義するクラス名が、DB 内のテーブル定義に該当する。
class Editor(models.Model):

    # note
    # ここに定義するクラス変数名が、DB 内のカラム定義に該当する。
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '名前', max_length = 255)
