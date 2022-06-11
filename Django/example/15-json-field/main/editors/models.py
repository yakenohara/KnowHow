from django.db import models

from common.utilities import StrChoiceEnum

# Create your models here.

# note
# ここに定義するクラス名が、DB 内のテーブル定義に該当する。
class Editor(models.Model):

    # note
    # ここに定義するクラス変数名が、DB 内のカラム定義に該当する。
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '名前', max_length = 255, unique = True)

    def __str__(self):
        return self.name

    class Sex(StrChoiceEnum):
        MALE = ('male', '男性')
        FEMALE = ('female', '女性')
    
    sex = models.CharField(verbose_name = '性別', max_length = 8, choices = Sex.choices(), null = True, blank = True)
    # note
    # null, blank の意味は以下の通り
    # null = True (デフォルトは False) : データベースに保存される値は必須ではない
    # blank = True (デフォルトは False) : フォームから投稿するときにこのフィールドの入力は必須ではない

    # note
    # 以下のように宣言して、宣言した関数で独自に実装した値を return すれば、
    # このモデルを扱う側からはプロパティにアクセスしたように振る舞う事ができる
    # ```
    # @property
    # def sexForView(self):
    # ```
    @property
    def sexForView(self):
        """
        WebUI 用の性別表示文字列を返す
        未設定の場合は空文字列を返す
        """
        return dict(Editor.Sex.choices()).get(self.sex, '')
