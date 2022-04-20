from django.db import models

from authors.models import Author
# Create your models here.

class Book(models.Model):
    id = models.AutoField(verbose_name = 'ID', primary_key = True)
    name = models.CharField(verbose_name = '著書名', max_length = 255, unique = True)
    author = models.ForeignKey(Author, verbose_name = '著者名', on_delete = models.SET_NULL, null = True, blank = True)
    # note
    #
    # `on_delete` で設定可能なパラメーター
    # https://docs.djangoproject.com/en/4.0/ref/models/fields/#foreignkey
    #
    #  - models.CASCADE
    #    紐付けられた外部キーオブジェクトが削除された時、自身のオブジェクトも削除する。
    #    e.g.
    #    Author オブジェクト "川端康成" を削除したとき、
    #    外部キーで紐づけた Book オブジェクト"雪の国", "伊豆の踊り子" オブジェクトも削除する
    #
    #  - models.PROTECT
    #    紐づけたオブジェクトが存在する場合は、削除ができない。削除しようとすると、django.db.models.ProtectedError が発生する。
    #    e.g.
    #    Author オブジェクト "川端康成" を削除しようとすると、
    #    外部キーで紐づけた Book オブジェクト "雪の国", "伊豆の踊り子" オブジェクトが存在するので削除できない。
    #
    #  - models.RESTRICT
    #    実例で示す。以下のようなモデル定義があった場合、
    #    ```
    #    class Artist(models.Model):
    #        name = models.CharField(max_length=10)
    #    class Album(models.Model):
    #        artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    #    class Song(models.Model):
    #        artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    #        album = models.ForeignKey(Album, on_delete=models.RESTRICT)
    #    ```
    #    以下のような振る舞いとなる。KnowHow/Django/assets/images/on-delete-restrict.svg に図による説明を示した。
    #    ```
    #    >>> artist_one = Artist.objects.create(name='artist one')
    #    >>> artist_two = Artist.objects.create(name='artist two')
    #    >>> album_one = Album.objects.create(artist=artist_one)
    #    >>> album_two = Album.objects.create(artist=artist_two)
    #    >>> song_one = Song.objects.create(artist=artist_one, album=album_one)
    #    >>> song_two = Song.objects.create(artist=artist_one, album=album_two)
    #    >>> album_one.delete()
    #    # Raises RestrictedError.
    #    >>> artist_two.delete()
    #    # Raises RestrictedError.
    #    >>> artist_one.delete()
    #    (4, {'Song': 2, 'Album': 1, 'Artist': 1})
    #    ```
    #
    #  - models.SET_NULL
    #    紐付けられた外部キーオブジェクトが削除された時、紐づけたオブジェクトのフィールドに null を設定する。
    # 
    #  - models.SET_DEFAULT
    #    紐付けられた外部キーオブジェクトが削除された時、`default = ~` に設定された値がセットされる。
    # 
    #  - models.models.SET(~)
    #    紐付けられた外部キーオブジェクトが削除された時、`.SET(~)` 内に指定した処理を実行する。
    #
    #  - models.DO_NOTHING
    #    紐付けられた外部キーオブジェクトが削除された時、なんの処理もしない。
