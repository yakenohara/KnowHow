# 前提

## 使用する OS Version

| OS      | Version                                                |
| ------- | ------------------------------------------------------ |
| Windows | Windows 10 Pro 21H2 (Windows 10 November 2021 Update ) |
| Mac     | Big Sur (バージョン 11.6.5                             |

## (仮想環境でない通常の) Python バージョン

| OS      | Version  |
| ------- | -------- |
| Windows | 3.8.8rc1 |
| Mac     | 3.8.8    |

##  (仮想環境でない通常の) Python パッケージバージョン

| Package    | Version |
| ---------- | ------- |
| pip        | 20.2.3  |
| virtualenv | 20.13.3 |

## 仮想環境にインストールする Python パッケージバージョン

| Package              | Version |
| -------------------- | ------- |
| Django               | 4.0.3   |
| django-bootstrap5    | 21.3    |
| django-widget-tweaks | 1.4.12  |
| djangorestframework  | 3.13.1  |
| python-dateutil      | 2.8.2   |
| drf-spectacular      | 0.22.0  |
| coverage             | 6.3.2   |

## JavaScript ライブラリバージョン

| ライブラリ | Version |
| ---------- | ------- |
| jQuery     | 3.6.0   |
| Bootstrap  | 5.1.3   |

# 環境のセットアップ・PJ の作成

Python の仮想環境を作成してから、仮想環境に Django, django-bootstrap 等を入れた後、PJ を作成する。  
OS 毎に方法が異なるので、対応する手順を参照。  

Windows の場合は [setup-windows10.md](setup-windows10.md) を参照。  
Mac の場合は [setup-mac-os-x.md](setup-mac-os-x.md) を参照。  

# 新しいアプリケーション

作成した Project 内の manage.py が配置してあるディレクトリで、`python manage.py startapp <アプリ名>` と実行する。  

```terminal
# note
# アプリケーションは、python でいうところのパッケージに相当する。
# そのため、パッケージの命名規則は PEP 8 に従い、すべて小文字で作成するのが一般的
# PEP 8
# https://peps.python.org/pep-0008/#package-and-module-names
D:\yakenohara\KnowHow\Django\example\02-basic\main>"D:\pyvenv\Scripts\python.exe" manage.py startapp editors

D:\yakenohara\KnowHow\Django\example\02-basic\main>
```

## アプリケーションの登録

main/settings.py を以下のように変更する。  

 - 変更前
```python
from pathlib import Path
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

 - 変更後
```python
import os # <-追加
from pathlib import Path
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5', # テンプレートファイル内で `{% load bootstrap5 %}` するなら左記のように追記
    'widget_tweaks', # テンプレートファイル内で `{% load widget_tweaks %}` するなら左記のように追記
    'editors', # `~python.exe manage.py startapp xxx` で作成したアプリ名
]
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # PJ 配下の `templates` ディレクトリを、テンプレートが配置されたディレクトリとして認識させる
        'APP_DIRS': True,
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), # PJ 配下の `static` ディレクトリを、テンプレートが使用するCSS ファイルや JavaScript ファイルが配置されたディレクトリとして認識させる
]

```

main/urls.py を以下の様に変更する。  

 - 変更前
```python
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

 - 変更後
```python
from django.urls import path, include # <- `include` を追加

urlpatterns = [
    path('admin/', admin.site.urls),

    # note
    # 第1引数には ``<`~python.exe manage.py startapp xxx` で作成したアプリ名>/`` を指定
    # 第2引数には ``include('<`~python.exe manage.py startapp xxx` で作成したアプリ名>.urls')`` を指定
    path('editors/', include('editors.urls')),
]
```

## アプリケーションの作り込み

アプリケーションの実装は大きく分けて以下 3 点で構成される。

 - URL スキームの設計

    Web サイト内での `http~/foo/bar/` という URL に対して、どのような関数やクラスを紐付けるかを定義することを、「URL スキームを設計する」という。  
    urls.py 内に定義する。

 -  モデル定義・フィールド定義
    
    Web サイトが使用する DB 内のテーブルの定義をすることを、「モデル定義をする」という。  
    各モデルは DB でいうところの、カラム定義をもっており、このカラムのことを、「フィールド」という。  
    models.py 内に定義する。  

 -  View 定義

    URL スキームに定義づけられた関数やクラスを定義することを「View を定義する」という。  
    view.py, および独自にファイルを追加して定義する forms.py に定義する。  


最もかんたんな実装例を example/02-basic/main/editors 配下に作成した。各ファイル間の関係性は下図のようになっている。  

![](assets/images/relations-python.svg)  

## html ファイルの作り込み

アプリが使用する html ファイルを templates ディレクトリに作成していく。  
最もかんたんな実装例を example/02-basic/main/templates 配下に作成した。各ファイル間の関係性は下図のようになっている。  

![](assets/images/relations-html.svg)  

### main/settings.py, main/urls.py, アプリの URL スキーム、動作定義と html ファイルの関係性

![](assets/images/relations-all.svg)  

# マイグレーション

アプリケーションの作り込みをしたら、models.py に定義したテーブル定義、カラム定義を DB に反映させるためのファイルである、"マイグレートファイル" を作成する。  
manage.py が配置されたディレクトリで、`python manage.py makemigrations` する。  

```terminal
D:\yakenohara\KnowHow\Django\example\02-basic\main>"D:\pyvenv\Scripts\python.exe" manage.py makemigrations
Migrations for 'editors':
  editors\migrations\0001_initial.py
    - Create model Editor

D:\yakenohara\KnowHow\Django\example\02-basic\main>
```
その後、`python manage.py migrate` する。  
```terminal
D:\yakenohara\KnowHow\Django\example\02-basic\main>"D:\pyvenv\Scripts\python.exe" manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, editors, sessions
Running migrations:
  Applying editors.0001_initial... OK

D:\yakenohara\KnowHow\Django\example\02-basic\main>
```

## 動作確認

ここまでくれば、`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/editors/` にアクセスしてみよう。  
下図のようなページが表示されるはずだ。  

![](assets/images/2022-03-21-20-21-03.png)  

`追加` ボタンを押せば下図のように追加画面に遷移し、名前を入力して `登録` ボタンを押せば、  

![](assets/images/2022-03-21-20-27-18.png)  

登録した名前がリストに反映されるはずだ。

![](assets/images/2022-03-21-20-29-59.png)  

`編集` ボタンを押せば、編集画面に遷移し、  

![](assets/images/2022-03-21-20-31-53.png)  

`削除` ボタンを押せば該当の "編集者" が削除される。  

## ここまでのソースコード

`django-admin startproject main` と `python manage.py startapp editors` 実行直後の環境を example/01-clean/main 配下に置いた。example/02-basic/main との差分を確認すれば、具体的にどのような実装をしたのかがわかるだろう。  

# 重複不可能なフィールド・バリデーションエラーハンドリング・テンプレートファイル間のオブジェクトの受け渡し

DB でいうところの、カラムにおいて、同じ値を受け付けないようにすることができる。  
models.py のフィールド定義を以下のように変更する。  

 - 変更前
```python
    name = models.CharField(verbose_name = '名前', max_length = 255)
```
 - 変更後
```python
    name = models.CharField(verbose_name = '名前', max_length = 255, unique = True)
```

ユーザーが WebUI において重複した値を入力して登録した場合は、フィールドに対してエラーが返ってくる。このようにエラーが発生することを、バリデーションエラーが発生したという。  
受け取ったバリデーションエラーを WebUI 画面上に表示させるように、フィールドオブジェクトの `.errors` プロパティを参照する templates/form.html を定義し、templates/editors/form.html では `{% include "form.html" with obj_field=form.name %}` のようにしてフィールドオブジェクトを templates/form.html に渡すようにしてみよう。  
以下例では、templates/editors/form.html の `{% include "form.html" with obj_field=form.name str_help_message="~" %}` のようにヘルプメッセージも付加して渡し、それを受け取った templates/form.html 側で「？」記号の `<<i title="~">` に指定して、さらにフィールドが入力必須の場合は「※」記号を表示している。  

![](assets/images/relations-html-03-no-duplication.svg)  

ファイルの準備ができたら、`python manage.py makemigration`, `python manage.py migrate` する。  

```terminal
D:\yakenohara\KnowHow\Django\example\03-no-duplication\main>"D:\pyvenv\Scripts\python.exe" manage.py makemigrations
Migrations for 'editors':
  editors\migrations\0002_alter_editor_name.py
    - Alter field name on editor

D:\yakenohara\KnowHow\Django\example\03-no-duplication\main>"D:\pyvenv\Scripts\python.exe" manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, editors, sessions
Running migrations:
  Applying editors.0002_alter_editor_name... OK

D:\yakenohara\KnowHow\Django\example\03-no-duplication\main>
```

`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/editors/create/` にアクセスすれば、下図のようになる。  

![](assets/images/2022-03-22-17-23-11.png)  

他のレコードと重複した名前を入力すれば、テキストエリア下部にエラーメッセージが表示されるはずだ。  

![](assets/images/2022-03-22-17-27-57.png)  

## ここまでのソースコード

この項で実装したソースコードを、example/03-no-duplication/main に置いた。  

# 削除確認ダイアログ

削除ボタンを押下した時に、削除を実行するかどうかを尋ねるダイアログを出すには、Bootstrap の機能を利用するのが簡単だ。  
templates/editors/list.html を以下の様に編集する。  

 - templates/editors/list.html
```html
{% extends "base.html" %}

{% block title %}編集者の一覧{% endblock title %}

{% block content %}
    <h4 class="mt-4 border-bottom">編集者の一覧</h4>
    <a href="{% url 'editors:create' %}" class="btn btn-primary btn-sm my-3">追加</a>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {# views.py の `class EditorsList(ListView):` で、 #}
        {# `model = Editor` することで `object_list` に、 #}
        {# models.py の `class Editor(models.Model):` 達が入る #}
        {% for editor in object_list %}
        <tr>
          <th scope="row">{{ editor.id }}</th>
          <td>{{ editor.name }}</td>
          <td>
            <a href="{% url 'editors:update' editor.id %}" class="btn btn-outline-primary btn-sm">編集</a>
            
            <!-- フィールド `id` を javascript で使用したいため、`data-??` を使用して渡す -->
            <!-- https://developer.mozilla.org/ja/docs/Web/API/HTMLElement/dataset -->
            <a href="javascript:void(0)" data-id="{{ editor.id }}" data-delete_confirmation_message="編集者 {{ editor.name }} を削除しますか？" class="btn btn-outline-primary btn-sm delete-btn">削除</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    
    <!-- 削除を確認するモーダルダイアログ -->
    {# https://getbootstrap.jp/docs/5.0/components/modal/ #}
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">削除確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p id="delete-confirmation-message"></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
            <button type="button" class="btn btn-primary" id="deletion-submitted">削除</button>
          </div>
        </div>
      </div>
    </div>
{% endblock content %}
{% block scripts %}
<script>
  $(document).ready(()=>{

    // レコードの削除
    $('.delete-btn').on('click', function(){ // 削除ボタンクリック時

      $('#delete-confirmation-message').text(this.dataset.delete_confirmation_message);
      $('#deleteModal').modal('show'); // `.modal('show')` の意味は右参照 https://getbootstrap.jp/docs/4.2/components/modal/
      $('#deletion-submitted').off('click'); // 重複して登録しないように、'click' イベントが存在する場合は削除
      $('#deletion-submitted').on('click', null, this.dataset.id, function(obj_event){ // https://api.jquery.com/on/
        $('#deleteModal').modal('hide'); // `.modal('hide')` の意味は右参照 https://getbootstrap.jp/docs/4.2/components/modal/

        // 削除用 URL を POST で叩く
        $.ajax({
          url: '/editors/' + obj_event.data + '/delete/',
          method: 'POST',
          
          // Setting the token on the AJAX request
          // https://docs.djangoproject.com/en/4.0/ref/csrf/#setting-the-token-on-the-ajax-request
          headers: {'X-CSRFToken': dict_utilities.getValueFromCookie('csrftoken')},
        }).done(() =>{
          location.reload();
        });

      });
    });
  });
</script>
{% endblock scripts %}
```

`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/editors` にアクセスして、適当なレコードを登録して、削除ボタンを押せば、下図のようになる。  

![](assets/images/2022-03-23-07-49-15.png)  

## ここまでのソースコード

この項で実装したソースコードを、example/04-delete-modal/main に置いた。  

# Choice フィールド

複数の候補からプルダウン形式で値を選択するフィールドの定義をしよう。  

## フィールド定義

まずは、モデル内のフィールド定義を行う。  
editors/models.py に以下のようにフィールドを追加する。

 - editors/models.py  
```python
    sex = models.CharField('性別', max_length = 8, choices = [('male', '男性'), ('female', '女性')], null = True, blank = True)
```

`choices = [(<DB内設定値>, <UI上表示値>), (<DB内設定値>, <UI上表示値>), ...]` という形で、フィールドに引数を設定する。しかしこのように `choices = ` にタプルの配列を定義するのはソースコードの見通しが悪くなる上、後でここに指定した配列を再利用するということが出来なくなる。そこで、Enum を利用して この配列を生成するのが望ましい。  
まわりくどい方法に感じるかもしれないが、common/utilities.py を新たに定義して、内容を以下のようにする。  

 - common/utilities.py  
``````python
import enum

def makeChoiceEnum(primitiveType):
    
    class _ChoiceEnum(primitiveType, enum.Enum):
        
        def __new__(cls, var_inDB, var_inUI):
            """ クラスのインスタンス生成 """
            obj = primitiveType.__new__(cls, var_inDB) # 指定されたプリミティブ型でインスタンスを生成
            obj._value_ = var_inDB # .value で値を取得できるように設定
            obj.choice = (var_inDB, var_inUI)
            return obj

        @classmethod
        def choices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(x, y), (a, b), ...] の形式にして返す
            """
            return [element.choice for element in cls]

    return _ChoiceEnum # インスタンス化せずにクラスそのものを返す

# str と enum.Enum を多重継承したクラス `class _ChoiceEnum(primitiveType, enum.Enum):` の定義
StrChoiceEnum = makeChoiceEnum(str)
"""
以下のように定義して使用する
## 定義方法
```
class Condition(StrChoiceEnum):
    NEW = ('new', '新品')   # <- この宣言時に `def __new__` が呼ばれる。以降同様。
    NOS = ('nos', '新古品') # new old stock
    USED = ('used', '中古')
```
## 使用方法
 - 'new' を取得するには、`Condition.NEW.value` もしくは `Condition.NEW.choice[0]`
 - '新品' を取得するには `Condition.NEW.choice[1]`
 - [('new', '新品'), ('nos', '新古品'), ('used', '中古')] を取得するには、`Condition.choices()`
"""
``````
そして、editors/models.py を以下の様に定義する。

 - editors/models.py  
```python
from django.db import models

from common.utilities import StrChoiceEnum # <- 追加

# Create your models here.

# note
# ここに定義するクラス名が、DB 内のテーブル定義に該当する。
class Editor(models.Model):

    # note
    # ここに定義するクラス変数名が、DB 内のカラム定義に該当する。
    id = models.AutoField(verbose_name = 'id', primary_key = True)
    name = models.CharField(verbose_name = '名前', max_length = 255, unique = True)

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
```
フィールドを追加したので、editors/forms.py に `'sex',` を以下のように追加する。  

 - editors/forms.py  
```python
class EditorEditForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = (
            'name',
            'sex', # <- 追加
        )
```

## html ファイルの作り込み

フォームの入力に使用する templates/editors/form.html に以下の様に定義を追加する。

 - templates/editors/form.html  
```html
      {# note #}
      {# `field=form.name` の `=` にはスペースをいれてはならない #}
      {% include "form.html" with obj_field=form.name str_help_message="編集者の名前を入力します。"%}
      {% include "form.html" with obj_field=form.sex str_help_message="任意で編集者の性別を入力します。"%}<!--  <- 追加 -->
```
`{% include "form.html" with obj_field=form.sex ~` で `sex` フィールドオブジェクトを受け取る templates/form.html では以下の様に定義を変更する
 - 変更前
```html
    {% else %}
    {{ obj_field | add_class:"form-control"}}{# `form-control` の意味は右参照 https://getbootstrap.jp/docs/5.0/forms/form-control/ #}
    {% endif %}
```
 - 変更後
```html
    {% else %}
    {% if obj_field.widget_type == 'select' %}{# `widget_type` の意味は右参照 https://docs.djangoproject.com/ja/4.0/ref/forms/api/#django.forms.BoundField.widget_type #}
    {{ obj_field | add_class:"form-select"}}{# `form-select` の意味は右参照 https://getbootstrap.jp/docs/5.0/forms/select/ #}
    {% else %}
    {{ obj_field | add_class:"form-control"}}{# `form-control` の意味は右参照 https://getbootstrap.jp/docs/5.0/forms/form-control/ #}
    {% endif %}
    {% endif %}
```
templates/editors/list.html は以下の様に変更する。  

 - 変更前
```html
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {# views.py の `class EditorsList(ListView):` で、 #}
        {# `model = Editor` することで `object_list` に、 #}
        {# models.py の `class Editor(models.Model):` 達が入る #}
        {% for editor in object_list %}
        <tr>
          <th scope="row">{{ editor.id }}</th>
          <td>{{ editor.name }}</td>
          <td>
            <a href="{% url 'editors:update' editor.id %}" class="btn btn-outline-primary btn-sm">編集</a>
```
 - 変更後
```html
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">性別</th><!--  <- 追加 -->
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {# views.py の `class EditorsList(ListView):` で、 #}
        {# `model = Editor` することで `object_list` に、 #}
        {# models.py の `class Editor(models.Model):` 達が入る #}
        {% for editor in object_list %}
        <tr>
          <th scope="row">{{ editor.id }}</th>
          <td>{{ editor.name }}</td>
          <td>{% if editor.sexForView %}{{ editor.sexForView }}{% else %} - {% endif %}</td><!--  <- 追加 -->
          <td>
            <a href="{% url 'editors:update' editor.id %}" class="btn btn-outline-primary btn-sm">編集</a>
```

## マイグレーション

フィールドを追加したので、`python manage.py makemigrations`, `python manage.py migrate` する。  
```terminal
D:\yakenohara\KnowHow\Django\example\05-choice-field\main>"D:\pyvenv\Scripts\python.exe" manage.py makemigrations
Migrations for 'editors':
  editors\migrations\0003_editor_sex.py
    - Add field sex to editor

D:\yakenohara\KnowHow\Django\example\05-choice-field\main>"D:\pyvenv\Scripts\python.exe" manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, editors, sessions
Running migrations:
  Applying editors.0003_editor_sex... OK
```

## 動作確認

`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/editors/` にアクセスすれば、`性別` 列が追加されたリストが表示される。  

![](assets/images/2022-03-23-09-29-58.png)  

`http://127.0.0.1:8000/editors/create/` では、性別がプルダウンで選択でき、未選択状態でも登録ができる。  

![](assets/images/2022-03-23-09-32-12.png)  
![](assets/images/2022-03-23-11-57-53.png)  

## ここまでのソースコード

この項で実装したソースコードを、example/05-choice-field/main に置いた。  

# CSV 入出力・ファイルへのログ出力

DB の内容を CSV ファイルとして出力する機能と、CSV で指定されたデータを DB に反映する機能を実装しよう。また、CSV で指定されたデータを DB に反映する際は、エラーが発生する可能性があるため、エラー発生時のエラー内容をユーザが把握できるように、ログファイルにエラーメッセージを出力する機能を実装しよう。  

## URL スキームの設計

editors/urls.py 内において、`export_as_csv` と `import_from_csv` を新たに追記する。  

 - 変更前
```python
from django.urls import path

from . import views

app_name = 'editors'
urlpatterns = [
    path('create/', views.EditorCreate.as_view(), name = 'create'),
    path('', views.EditorsList.as_view(), name = 'list'), # Read
    path('<int:pk>/update/', views.EditorUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', views.EditorDelete.as_view(), name = 'delete'),
]
```
 - 変更後
```python
from django.urls import path

from . import views

app_name = 'editors'
urlpatterns = [
    path('create/', views.EditorCreate.as_view(), name = 'create'),
    path('', views.EditorsList.as_view(), name = 'list'), # Read
    path('<int:pk>/update/', views.EditorUpdate.as_view(), name = 'update'),
    path('<int:pk>/delete/', views.EditorDelete.as_view(), name = 'delete'),
    path('export_as_csv/', views.export_as_csv, name = 'export_as_csv'),
    path('import_from_csv/', views.import_from_csv, name = 'import_from_csv'),
]
```

## モデル定義・フィールド定義

CSV ファイル内に定義された各行 (DB 内におけるレコードに相当するもの) は、View 定義においてバリデーションされてレコードとして登録される。今回実装する `Editor` モデルはすでに定義済みなので、ここでは新たな実装は必要ない。  

## View 定義

まずは、共通で使用する各種定数定義を common/const.py を作成して以下のように定義する。  

 - common/const.py  
```python
#
# ログファイルフォルダ名
STR_LOG_FOLDER_NAME = 'log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_INFO = 'info.log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_WARNING = 'warning.log'

#
# ログファイル名(INFO Level 以上)
STR_LOG_FILE_NAME_ERROR = 'error.log'

#
# デッドロック検知時にリトライする回数
INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK = 32

#
# デッドロック検知時にリトライするために sleep する時間 [s]
FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK = 0.1
```

次に、common/utilities.py において、CSV ファイル内で `男性` / `女性` のように選択式のフィールドの値が、`男性` / `女性` のいずれかであることを確認する機能を実装するために必要となる、`[('male', '男性'), ('female', '女性')]` のタプル配列内の各要素を逆転させて、`[('男性', 'male'), ('女性', 'female')]` という配列を生成することができる `def makeChoiceEnum(primitiveType):` 内の新たなクラスメソッドや、今後共通で使用することになる関数を以下の様に定義する。

 - 変更前
``````python
import enum

def makeChoiceEnum(primitiveType):
    
    class _ChoiceEnum(primitiveType, enum.Enum):
        
        def __new__(cls, var_inDB, var_inUI):
            """ クラスのインスタンス生成 """
            obj = primitiveType.__new__(cls, var_inDB) # 指定されたプリミティブ型でインスタンスを生成
            obj._value_ = var_inDB # .value で値を取得できるように設定
            obj.choice = (var_inDB, var_inUI)
            return obj

        @classmethod
        def choices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(x, y), (a, b), ...] の形式にして返す
            """
            return [element.choice for element in cls]

    return _ChoiceEnum # インスタンス化せずにクラスそのものを返す

# str と enum.Enum を多重継承したクラス `class _ChoiceEnum(primitiveType, enum.Enum):` の定義
StrChoiceEnum = makeChoiceEnum(str)
"""
以下のように定義して使用する
## 定義方法
```
class Condition(StrChoiceEnum):
    NEW = ('new', '新品')   # <- この宣言時に `def __new__` が呼ばれる。以降同様。
    NOS = ('nos', '新古品') # new old stock
    USED = ('used', '中古')
```
## 使用方法
 - 'new' を取得するには、`Condition.NEW.value` もしくは `Condition.NEW.choice[0]`
 - '新品' を取得するには `Condition.NEW.choice[1]`
 - [('new', '新品'), ('nos', '新古品'), ('used', '中古')] を取得するには、`Condition.choices()`
"""
``````
 - 変更後
``````python
import csv
import enum
import io

def makeChoiceEnum(primitiveType):
    
    class _ChoiceEnum(primitiveType, enum.Enum):
        
        def __new__(cls, var_inDB, var_inUI):
            """ クラスのインスタンス生成 """
            obj = primitiveType.__new__(cls, var_inDB) # 指定されたプリミティブ型でインスタンスを生成
            obj._value_ = var_inDB # .value で値を取得できるように設定
            obj.choice = (var_inDB, var_inUI)
            obj.reversedChoice = (var_inUI, var_inDB) # `.choice` のタプル内要素逆転版
            return obj

        @classmethod
        def choices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(x, y), (a, b), ...] の形式にして返す
            """
            return [element.choice for element in cls]

        @classmethod
        def reversedChoices(cls):
            """
            クラスに定義された 2 つの要素をもったタプルを、
            [(y, x), (b, a), ...] の形式にして返す
            `def choices(cls):` のタプル内要素逆転版。
            """
            return [element.reversedChoice for element in cls]

    return _ChoiceEnum # インスタンス化せずにクラスそのものを返す

# str と enum.Enum を多重継承したクラス `class _ChoiceEnum(primitiveType, enum.Enum):` の定義
StrChoiceEnum = makeChoiceEnum(str)
"""
以下のように定義して使用する
## 定義方法
```
class Condition(StrChoiceEnum):
    NEW = ('new', '新品')   # <- この宣言時に `def __new__` が呼ばれる。以降同様。
    NOS = ('nos', '新古品') # new old stock
    USED = ('used', '中古')
```
## 使用方法
 - 'new' を取得するには、`Condition.NEW.value` もしくは `Condition.NEW.choice[0]`
 - '新品' を取得するには `Condition.NEW.choice[1]`
 - [('new', '新品'), ('nos', '新古品'), ('used', '中古')] を取得するには、`Condition.choices()`
"""

def makeVerboseNameVsFieldNameDict(obj_model):
    """
    モデルから verbose_name とフィールド名の対応表を作成して返す
    """
    dict_fieldNameVsVerboseName = {}
    for meta_field in obj_model._meta.get_fields():
        str_verbose_name = obj_model._meta.get_field(meta_field.name).verbose_name
        dict_fieldNameVsVerboseName[str_verbose_name] = meta_field.name
    
    return dict_fieldNameVsVerboseName

def makeCSVStringFromDict(dict_models, str_columnDefinitions):
    """
    モデルを辞書配列化したものを CSV 文字列化する
    """
    str_csv = ''
    with io.StringIO() as stream:
        writer = csv.writer(stream)
        writer.writerow(str_columnDefinitions)
        for dict_model in dict_models:
            writer.writerow(dict_model.values())

        # BOM 付き UTF-8 文字列を取得
        str_csv = stream.getvalue().encode('utf-8-sig')
    return str_csv

def getOrdinalString(int_number):
    """
    数値を序数詞 (1st, 2nd, 3rd 等) の文字列にして返す
    """
    return str(int_number) + {1: "st", 2: "nd", 3: "rd"}.get((int_number if 10 < int_number < 14 else int_number % 10), "th")
``````
次に、CSV ファイル内に定義された各行が期待したモデル定義にマッチするかどうかを確認する機能を実装するため、editors/forms.py 内に以下のようにフォーム定義を追加する。  
(新たに必要となる `MinValueValidator` 等のモジュールは、必要に応じてファイル冒頭で import する。詳しくは example/06-input-out-CSV/main/editors/forms.py 参照)  

 - editors/forms.py  
```python
class EditorCSVForm(forms.Form):
    
    id = forms.IntegerField(
        validators = [
            # note
            # editors/models.py -> class Editor(models.Model): で
            # `id = models.AutoField` と定義している。
            # `AutoField` は `-2147483648 to 2147483647 are safe` とのことなので、この範囲を有効範囲とする
            # https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.IntegerField
            MinValueValidator(limit_value = -2147483648, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
            MaxValueValidator(limit_value = 2147483647, message = 'ID は -2147483648 から 2147483647 の範囲を指定してください。'),
        ]
    )
    name = forms.CharField(max_length = 255)

    #
    # CSV ファイル内には、タプル定義の2要素目が定義されている。
    # その為、このフィールドの `choices = ~` の定義は `[('男性', 'male'), ('女性', 'female') ...]` のように
    # タプル要素の 1 つめと 2 つめを逆転させた定義が必要なので、
    # common/utilities.py -> `def makeChoiceEnum(primitiveType):` -> `class _ChoiceEnum(primitiveType, enum.Enum):` 内に新たに定義した、
    # `def reversedChoices(cls):` を使ってタプル内要素を逆転させた配列を取得している
    sex = forms.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False)

    #
    # `class EditorCSVForm(forms.Form):` の `.is_valid()` 実行によるバリデーション確認時にコールされる。  
    # `class EditorEditForm(forms.ModelForm):` のように、`def clean(self):` を定義しなくても、
    # バリデーションが行われるが、`sex` フィールドに定義された '男性'/'女性'/'' -> 'male'/'female'/None へ変換するため、  
    # このように定義することでバリデーション機能をオーバーライドできる。  
    def clean(self):

        # Django が提供するデフォルトのバリデーション機能を実行させるため、
        # このように記載する。  
        cleaned_data = super().clean()

        # `sex` フィールドに定義された '男性'/'女性'/'' -> 'male'/'female'/None へ変換する
        cleaned_data['sex'] = dict(self.fields['sex'].choices).get(cleaned_data['sex'], None)
        #
        # note1
        # `sex = forms.ChoiceField(choices = [('男性', 'male'), ('女性', 'female')])` の `choices = ~` に設定したタプル配列を取得するには、
        # `self.fields['sex'].choices` のように記載することで取得できる
        #
        # note2
        # `sex` フィールドは CSV ファイル内で空文字が設定されていた場合、  
        # editors/models.py -> `class Editor(models.Model):` ->  `class Sex(StrChoiceEnum):` の `.reversedChoices()` を
        # 辞書化したディクショナリオブジェクトのプロパティに存在しないプロパティ '' (空文字列) を検索することになる。
        # KeyError を防ぐ為、`.get()` で取得する。  

        # オーバーライドしたバリデーション動作の結果をオブジェクトとして返す
        return cleaned_data
```

そして、モデル定義にマッチするかどうかを確認する機能内でエラーを発見した際にログファイルにそのエラー内容を出力できるように、main/settings.py に以下を追加する。  

 - `BASE_DIR = Path(__file__).resolve().parent.parent` 前後
```python
import os
from pathlib import Path
from common.const import STR_LOG_FOLDER_NAME, STR_LOG_FILE_NAME_INFO, STR_LOG_FILE_NAME_WARNING, STR_LOG_FILE_NAME_ERROR

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ログ保存用ディレクトリの作成
str_logDirectory = os.path.join(BASE_DIR, STR_LOG_FOLDER_NAME)
if not os.path.exists(str_logDirectory): # ディレクトリが存在しない場合
    os.mkdir(str_logDirectory) # ディレクトリ作成
```
 - ファイル後部

```python
# ログ出力設定
# <Pythonインストールパス>/Lib/site-packages/django/utils/log.py の `DEFAULT_LOGGING` を
# `LOGGING` としてここに定義すると、設定をオーバーライドできる。
# 
# https://docs.djangoproject.com/en/4.0/ref/logging/

LOGGING = {
    'version': 1, # 必須項目かつ有効な値は 1 のみ https://docs.python.org/ja/3/library/logging.config.html#dictionary-schema-details
    'disable_existing_loggers': False, # 公式ドキュメントの `DEFAULT_LOGGING` のまま `False` にしておく

    # 出力フォーマット定義
    'formatters': {
        'simple': { # 'simple' という名称のフォーマットを定義
            # 使用可能な属性は以下参照
            # https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
            'format': "%(asctime)s [%(levelname)s] %(message)s"
        },
    },

    # ログの出力先を設定する（標準出力、ファイル、メール等
    # この設定のことをハンドラーという。  
    'handlers': {
        'info': { # 'info' という名称のハンドラーを定義
            'level': 'INFO', # ログレベル
            'class': 'logging.FileHandler', # https://docs.python.org/ja/3/library/logging.handlers.html#filehandler
            'filename': os.path.join(BASE_DIR, STR_LOG_FOLDER_NAME, STR_LOG_FILE_NAME_INFO),
            'encoding': 'utf-8',
            'formatter': 'simple', # 'simple' という名称のフォーマットを使用
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, STR_LOG_FOLDER_NAME, STR_LOG_FILE_NAME_WARNING),
            'encoding': 'utf-8',
            'formatter': 'simple',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, STR_LOG_FOLDER_NAME, STR_LOG_FILE_NAME_ERROR),
            'encoding': 'utf-8',
            'formatter': 'simple',
        },
    },

    # アプリケーション毎に異なるハンドラー定義を行う場合は、以下の様に定義
    # 'loggers': {
    #     'django.server': {
    #         'handlers': ['info', 'mail_admins'],
    #         'level': 'INFO',
    #     },
    #     'django': {
    #         'handlers': ['django.server'],
    #         'level': 'INFO',
    #         'propagate': False,
    #         # 
    #         # note
    #         # `'propagate': False` すると、上位の定義に伝搬させない。
    #         # この場合の親子関係は、親-> 子 -> 孫 の順に、以下のようになる
    #         # `root` -> `django` -> `django.server`
    #         # 例えば、以下のような実装を行うと
    #         # ```
    #         # logger = logging.getLogger("django.server")
    #         # logger.info("hoge")
    #         # ```
    #         # ```
    #     },
    # },
    'root': {
        'handlers': ['info', 'warning', 'error'],
        'level': 'INFO', # ログレベル
    },
}
```
これで CSV 入出力の機能を実装する準備が整った。CSV 入出力の機能は editors/views.py 内に以下の様に実装する。  
(新たに必要となる `logging` 等のモジュールは、必要に応じてファイル冒頭で import する。詳しくは example/06-input-out-CSV/main/editors/views.py 参照)  

 - ファイル冒頭
```python
# note  
# `__name__` には自身のモジュール名が入る。  
# この場合は `editors.views` という文字列。  
logger = logging.getLogger(__name__)
```
 - ファイル後部
```python
def makeDictFromEditors(model_editors):
    """
    編集者リストを辞書配列化する
    """
    dict_editors = []
    for model_edtir in model_editors:
        dict_tmp = model_to_dict(model_edtir)
        dict_tmp['sex'] = dict(Editor.Sex.choices()).get(model_edtir.sex, '')
        dict_editors.append(dict_tmp)
    return dict_editors

@require_safe # https://docs.djangoproject.com/en/4.0/topics/http/decorators/#django.views.decorators.http.require_safe
def export_as_csv(request):
    
    # 
    # 以下の形式のディクショナリを生成
    # ```
    # {
    #     'ID' : 'id',
    #     '名前' : 'name',
    #     '性別' : 'sex',
    # }
    # ```
    dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Editor())

    obj_idSortedEditors = Editor.objects.all().order_by('id')
    dict_editors = makeDictFromEditors(obj_idSortedEditors) # 編集者リストを辞書配列化
    str_csv = makeCSVStringFromDict(dict_editors, dict_verboseNameVsFieldName.keys()) # 辞書配列を CSV 文字列化

    # CSV ファイルにして出力
    obj_response = HttpResponse(str_csv, content_type = 'text/csv; charsert=utf-8-sig')
    obj_response['Content-Disposition'] = 'attachment; filename="editors.csv"'

    return obj_response

@require_POST # https://docs.djangoproject.com/en/4.0/topics/http/decorators/#django.views.decorators.http.require_POST
def import_from_csv(request):
    
    obj_csvImportForm = CSVImputForm(request.POST, request.FILES)

    #
    # インスタンス化したフォームクラスの `.is_valid()` をコールすることで、  
    # バリデーションを確認することができる。  
    # ここでは、CSVImputForm のバリデーションエラーとなっていないかどうかを確認している。
    # 以下のようなパターンの場合に、バリデーションエラーとなる。  
    # e.g.
    #  - `mode` フィールドが存在しない
    #  - `mode` フィールドの値が `update` でも `replace` でもない
    #  - ファイルが指定されていない
    if not obj_csvImportForm.is_valid():
        for str_key, str_errmsgs in obj_csvImportForm.errors.items():
            logger.warning(f'{str_key}: "{str_errmsgs[0]}"')
        return redirect('editors:list') # 一覧へ遷移

    obj_toImportEditors = []
    str_fileName = request.FILES['file'].name
    with io.TextIOWrapper(request.FILES['file'], encoding = 'utf-8-sig') as stream:

        obj_reader = csv.DictReader(stream)

        try:
            str_verboseNamesInProbe = obj_reader.fieldnames
        except UnicodeDecodeError as err:
            # e.g. ファイルの文字コードが SJIS で保存されていた場合
            logger.warning(f'`UnicodeDecodeError` has occured while opening "{str_fileName}". Reason: "{err.reason}"')
            return redirect('editors:list') # 一覧へ遷移

        dict_verboseNameVsFieldName = makeVerboseNameVsFieldNameDict(Editor())
        str_requiredHeaders = dict_verboseNameVsFieldName.keys()

        # 必要なカラムタイトルが存在するかどうかチェック
        for str_requiredHeader in str_requiredHeaders:
            if str_requiredHeader not in str_verboseNamesInProbe:
                logger.warning(f'Required header `{str_requiredHeader}` is not defined in "{str_fileName}"')
                return redirect('editors:list') # 一覧へ遷移

        for dict_readRow in obj_reader:
            
            # 必要なプロパティ定義だけをもったディクショナリを生成
            dict_subject = {dict_verboseNameVsFieldName[str_verboseName]: dict_readRow[str_verboseName] for str_verboseName in dict_verboseNameVsFieldName.keys()}

            obj_subjectEditor = EditorCSVForm(dict_subject)

            if obj_subjectEditor.is_valid(): # バリデーション OK の場合
                obj_toImportEditors.append(obj_subjectEditor.cleaned_data)  

            else: # バリデーションエラーの場合
                str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in dict_readRow.items()])
                logger.warning(f'Validation error has occured while loading {str_tmp}. Check following.')
                for str_key, str_errmsgs in obj_subjectEditor.errors.items():
                    logger.warning(f'{str_key}: "{str_errmsgs[0]}"')

    #
    # トランザクション試行ループ。  
    # 複数ユーザーから同時にこの機能が実行されると、DB のデッドロックが発生する可能性があるため、  
    # SQL 文が発行されるコードは以下の `with transaction.atomic():` 内で記述し、  
    # デッドロックが発生した場合は `OperationalError` が発生するのでそれをキャッチ。  
    # 一定時間スリープしてリトライする。  
    bl_retrying = True
    int_tryTime = 1
    while bl_retrying:
        try:
            with transaction.atomic():
                # この with 文内で実行される SQL 文はまとめて実行される。

                # 全ての ID リストをここで取得し、レコードを更新する度にこのリストから ID を削除していく。
                dict_notUpdatedIDs = {obj_editors.id: obj_editors.id for obj_editors in Editor.objects.all()}

                for obj_toImportEditor in obj_toImportEditors:

                    try:
                        Editor.objects.update_or_create(
                            id = obj_toImportEditor['id'],
                            defaults = {
                                'name': obj_toImportEditor['name'],
                                'sex': obj_toImportEditor['sex'],
                            }
                        )
                        
                        # レコードを更新したのでリストから ID を削除
                        dict_notUpdatedIDs.pop(obj_toImportEditor['id'], None)

                    except IntegrityError as err: # `名前` フィールドが他レコードと重複した場合
                        str_tmp = ', '.join([f'{str_key}: "{var_val}"' for str_key, var_val in obj_toImportEditor.items()])
                        logger.warning(f'`IntegrityError` has occured while saving {str_tmp}. Check following.')
                        logger.warning(err)
                
                # `置き換え` モードの場合
                if obj_csvImportForm.cleaned_data.get('mode') == 'replace':
                    for int_notUpdatedID in dict_notUpdatedIDs.values():
                        Editor.objects.filter(id = int_notUpdatedID).first().delete()


        except OperationalError as err:
            # デッドロックの可能性。既定回数分リトライする。
            
            logger.warning(f'There is a possibility of deadlock. This is the {getOrdinalString(int_tryTime)} time attempt. Check following.')
            logger.warning(str(err))

            if int_tryTime <= INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK: # 既定回数以内の場合
                # スリープして再試行
                time.sleep(FL_SLEEP_TIME_OF_RETRYING_CAUSE_OF_DEADLOCK)
                int_tryTime += 1
                logger.warning('Transaction retrying...')
                continue

            else:
                logger.error(f'The number of record saving attempts has reached the upper limit ({INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK} times).')
        
        # `OperationalError` が発生しなかった場合または `OperationalError` が規定回数繰り返し発生した場合
        bl_retrying = False
    
    return redirect('editors:list')
```
## html ファイルの作り込み
一覧画面で `CSV 出力` と `CSV 入力` を実行できるよう、templates/editors/list.html を以下の様に変更する。  

 - templates/editors/list.html  
```html
{% extends "base.html" %}

{% block title %}編集者の一覧{% endblock title %}

{% block content %}
    <h4 class="mt-4 border-bottom">編集者の一覧</h4>
    <a href="{% url 'editors:create' %}" class="btn btn-primary btn-sm my-3">追加</a>
    <a href="{% url 'editors:export_as_csv' %}" class="btn btn-primary btn-sm my-3">CSV 出力</a>
    <button class="btn btn-primary btn-sm my-3" id="csv-input-btn">CSV 入力</button>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">性別</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {# views.py の `class EditorsList(ListView):` で、 #}
        {# `model = Editor` することで `object_list` に、 #}
        {# models.py の `class Editor(models.Model):` 達が入る #}
        {% for editor in object_list %}
        <tr>
          <th scope="row">{{ editor.id }}</th>
          <td>{{ editor.name }}</td>
          <td>{% if editor.sexForView %}{{ editor.sexForView }}{% else %} - {% endif %}</td>
          <td>
            <a href="{% url 'editors:update' editor.id %}" class="btn btn-outline-primary btn-sm">編集</a>
            
            <!-- フィールド `id` を javascript で使用したいため、`data-??` を使用して渡す -->
            <!-- https://developer.mozilla.org/ja/docs/Web/API/HTMLElement/dataset -->
            <a href="javascript:void(0)" data-id="{{ editor.id }}" data-delete_confirmation_message="編集者 {{ editor.name }} を削除しますか？" class="btn btn-outline-primary btn-sm delete-btn">削除</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    
    <!-- 削除を確認するモーダルダイアログ -->
    {# https://getbootstrap.jp/docs/5.0/components/modal/ #}
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">削除確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p id="delete-confirmation-message"></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
            <button type="button" class="btn btn-primary" id="deletion-submitted">削除</button>
          </div>
        </div>
      </div>
    </div>
    <!-- CSV 入力のモーダルダイアログ -->
    <div class="modal fade" id="CSVInputModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">CSV 入力</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form action="{% url "editors:import_from_csv" %}" enctype="multipart/form-data" method="post">
            <div class="modal-body">
              {% csrf_token %}
              <div class="mb-2">
                <input type="file" name="file" class="form-control" id="csv-input">{# `form-control` の意味は右参照 https://getbootstrap.jp/docs/5.0/forms/form-control/ #}
              </div>
              <div class="mb-2">
                <div class="form-check form-check-inline">{# https://getbootstrap.jp/docs/5.0/forms/checks-radios/#inline #}
                  <input class="form-check-input" type="radio" name="mode" id="inlineRadio1" value="update" checked>
                  <label class="form-check-label" for="inlineRadio1">更新及び追加</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" name="mode" id="inlineRadio2" value="replace">
                  <label class="form-check-label" for="inlineRadio2">置き換え</label>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
              <input type="submit" class="btn btn-primary" value="反映"></input>
            </div>
          </form>
        </div>
      </div>
    </div>
{% endblock content %}
{% block scripts %}
<script>
  $(document).ready(()=>{

    // レコードの削除
    $('.delete-btn').on('click', function(){ // 削除ボタンクリック時

      $('#delete-confirmation-message').text(this.dataset.delete_confirmation_message);
      $('#deleteModal').modal('show'); // `.modal('show')` の意味は右参照 https://getbootstrap.jp/docs/4.2/components/modal/
      $('#deletion-submitted').off('click'); // 重複して登録しないように、'click' イベントが存在する場合は削除
      $('#deletion-submitted').on('click', null, this.dataset.id, function(obj_event){ // https://api.jquery.com/on/
        $('#deleteModal').modal('hide'); // `.modal('hide')` の意味は右参照 https://getbootstrap.jp/docs/4.2/components/modal/

        // 削除用 URL を POST で叩く
        $.ajax({
          url: '/editors/' + obj_event.data + '/delete/',
          method: 'POST',
          
          // Setting the token on the AJAX request
          // https://docs.djangoproject.com/en/4.0/ref/csrf/#setting-the-token-on-the-ajax-request
          headers: {'X-CSRFToken': dict_utilities.getValueFromCookie('csrftoken')},
        }).done(() =>{
          location.reload();
        });

      });
    });

    // CSV 入力
    $('#csv-input-btn').on('click', function(){ // CSV 入力ボタンクリック時
      $('#CSVInputModal').modal('show');
    });
  });
</script>
{% endblock scripts %}
```

## 動作確認

`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/editors/` にアクセスすれば、`CSV 出力` と `CSV 入力` 機能が追加されたリストが表示される。  

 - CSV 出力  
![](assets/images/2022-04-01-10-31-48.png)  
 - CSV 入力(更新及び追加)  
![](assets/images/update-from-csv.svg)  
![](assets/images/2022-04-01-10-37-16.png)  
 - CSV 入力(置き換え)  
![](assets/images/replace-from-csv.svg)  
![](assets/images/2022-04-01-10-37-16.png)  
 - CSV 入力(エラー発生パターン)  
![](assets/images/update-from-csv-with-error-01.svg)  
![](assets/images/2022-04-01-12-09-47.png)  
![](assets/images/update-from-csv-with-error-02.svg)  

## ここまでのソースコード

この項で実装したソースコードを、example/06-input-out-CSV/main に置いた。  

# ユーザー認証・管理

ここまで `python manage.py createsuperuser` で作成したユーザーに関わる実装をしてこなかった。このままでは、どのユーザーからでも編集者の登録ができてしまう。また、この後の章で出てくる Token を使用した REST API の実装でユーザーの概念が必要になってくるので、ログインしていないユーザーに関してはログイン画面へリダイレクトさせてログインまたはユーザー登録を促し、ユーザー一覧画面で登録済みユーザーの消去、新規ユーザーの作成を行う機能を実装しよう。  

この機能を実装するにあたり、ユーザーがログイン後に最初に訪れるトップページを提供するアプリも同時に作成していく。  

## アプリケーションの作成

`# 新しいアプリケーション` の章で `editors` アプリを作ったのと同様にして、 `accounts` アプリと `index` アプリを作成する。  

```terminal
D:\yakenohara\KnowHow\Django\example\07-user-auth\main>"D:\pyvenv\Scripts\python.exe" manage.py startapp accounts

D:\yakenohara\KnowHow\Django\example\07-user-auth\main>"D:\pyvenv\Scripts\python.exe" manage.py startapp index

D:\yakenohara\KnowHow\Django\example\07-user-auth\main>
```

アプリの登録も、`editors` アプリの時と同様だ。

 - main/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5', # テンプレートファイル内で `{% load django_bootstrap5 %}` するなら左記のように追記
    'widget_tweaks', # テンプレートファイル内で `{% load widget_tweaks %}` するなら左記のように追記
    'editors', # `~python.exe manage.py startapp xxx` で作成したアプリ名
    'accounts', # <- ここを追加
    'index', # <- ここを追加
]
```
 - main/urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),

    # note
    # 第1引数には ``<`~python.exe manage.py startapp xxx` で作成したアプリ名>/`` を指定
    # 第2引数には ``include('<`~python.exe manage.py startapp xxx` で作成したアプリ名>.urls')`` を指定
    path('editors/', include('editors.urls')),
    path('accounts/', include('accounts.urls')), # <- ここを追加
    path('', include('index.urls')), # <- ここを追加
]
```

## URL スキームの設計

URL スキームの設計は、`accounts` アプリと `index` アプリでそれぞれ以下のように行う。  
(accounts/urls.py のように、`path()` に設定する第 2 引数の関数(これをView 関数という)を、views.py に定義した関数を指定するのではなく直で定義することもできる)  

 - accounts/urls.py  
```python
app_name = 'accounts'
urlpatterns = [
    path('signup/', CreateView.as_view(
        template_name = 'accounts/form.html',
        form_class = UserCreationForm,
        success_url = '/',
    ), name='signup'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user = True,
        # note
        # ログインページにアクセスする認証済みユーザーが、ログインに成功したかのようにリダイレクトさせる。
        # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.redirect_authenticated_user
        
        template_name = 'accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('', views.AccountsListView.as_view(), name = 'list'), # Read
    path('<int:pk>/delete/', views.AccountDelete.as_view(), name = 'delete'),
]
```
 - index/urls.py
```python
app_name = 'index'
urlpatterns = [
    path('', views.Index.as_view(), name = 'index')
]
```
## モデル定義・フィールド定義

`accounts` アプリと `index` アプリについてモデル定義をすると言いたいところだが、それぞれ以下の理由で作成する必要はない。  

 - `accounts` アプリ  
    Django がモデル `User` (`from django.contrib.auth.models import User` のように import することで使用できる) をデフォルトで提供してくれている。このモデルをそのまま使うことで、`accounts` アプリは自分で新たなユーザー用もモデル定義をする必要が無くなる。  

 - `index` アプリ  
    トップページを提供だけのアプリであり、この章では、このアプリ内で特段新たなモデルを定義する必要は無い。  

## View 定義

`accounts` アプリと `index` アプリについてそれぞれ以下のように実装する。  

 - accounts/views.py
```python
class AccountCreateView(CreateView):
    model = User
    template_name = 'accounts/form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:list')

class AccountsListView(ListView):
    model = User
    template_name = 'accounts/list.html'
    success_url = reverse_lazy('accounts:list')

class AccountDelete(DeleteView):
    model = User
    success_url = reverse_lazy('editors:list')
```
 - index/views.py
```python
class Index(TemplateView):
    template_name = 'index.html'
```

そして、"ログインしていないユーザーに関してはログイン画面へリダイレクトさせてログインまたはユーザー登録を促す" ロジックの作り込みをする。  
これは Django が提供する Middleware という機能を実装することによって実現できる。説明と同時にソースコードで示そう。  
新たなファイル common/middleware.py を作成して中を以下の様に記述する。  

 - common/middleware.py
```python
import re

from django.contrib.auth.decorators import login_required

from main.settings import STR_URL_EXCEPTION_THAT_REQUIRES_LOGIN

# https://docs.djangoproject.com/en/4.0/topics/http/middleware/#middleware
class LoginRequiredMiddleware:

    # サーバ起動時に1度だけ呼び出されるメソッド
    def __init__(self, get_response):
        self.get_response = get_response

        #
        # ここにサーバ起動時に1度だけ呼び出される処理を記載する
        #

        # ログインが不要な URL 文字列の正規表現一覧をコンパイルしてタプル化
        self.re_urlExceptionsThatRequiresLogin = tuple(re.compile(str_url) for str_url in STR_URL_EXCEPTION_THAT_REQUIRES_LOGIN)

    # リクエスト毎に呼び出されるメソッド
    def __call__(self, request):

        #
        # ここに view 関数適用前に実行する共通処理を定義する
        # 

        # `request` オブジェクトに対して view 関数を適用させて `response` オブジェクトを得る
        response = self.get_response(request)

        #
        # ここに view 関数の処理が終わった後に
        # レスポンスをサーバから返す前に実行する共通処理を定義する
        #

        return response

    #
    # view関数を呼び出す直前にhookされるメソッド。
    # `ここに view 関数適用前に実行する共通処理を定義する` のポイントで実行される処理と違い、  
    # 実行される view 関数(以下 `view_func`)、実行される view 関数への引数 (以下 `view_args, view_kwargs`) を取得できる  
    # https://docs.djangoproject.com/en/4.0/topics/http/middleware/#process-view
    def process_view(self, request, view_func, view_args, view_kwargs):

        # ログインが不要な URL にマッチするかどうかチェック
        for re_urlExceptionThatRequiresLogin in self.re_urlExceptionsThatRequiresLogin:
            if re_urlExceptionThatRequiresLogin.match(request.path): # ログインが不要な URL の場合
                return None

        #
        # ユーザーがログインしているかどうかをチェックして、ログインしていない場合は、
        # あらかじめ定められたログイン用 URL へリダイレクトさせるデコレーター `login_required` で装飾する
        # https://docs.djangoproject.com/en/4.0/topics/auth/default/#the-login-required-decorator
        #
        # `login_required` で装飾した view 関数を実行して返す(`HttpResponse` を返す)
        # `login_required(view_func)` としているのは、`view_func` にデコレーターが付与されていた場合、  
        # そのデコレーターを実行させるため。  
        return login_required(view_func)(request, *view_args, **view_kwargs)
```
そして、上記 `class LoginRequiredMiddleware:` 自体の Middleware としての登録と、必要となる定義値 `STR_URL_EXCEPTION_THAT_REQUIRES_LOGIN` 等の定義を main/settings.py に実装していく。  

 - main/settings.py
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.LoginRequiredMiddleware', # <- ここを追加
]
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~

# 以下 4 つの定義を追加

# `login_required()` デコレーターでログインされていないことがわかった場合のリダイレクト先
# https://docs.djangoproject.com/en/4.0/ref/settings/#login-url

LOGIN_URL = '/accounts/login/'

# `LoginView` でログインした後のリダイレクト先
# https://docs.djangoproject.com/en/4.0/ref/settings/#login-redirect-url

LOGIN_REDIRECT_URL = '/'

# `LogoutView` でログアウトした後のリダイレクト先
# https://docs.djangoproject.com/en/4.0/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ログインが不要な URL 文字列の正規表現一覧
STR_URL_EXCEPTION_THAT_REQUIRES_LOGIN = [
    r'/accounts/login/(.*)$',
    r'/accounts/signup/(.*)$',
]
```
これでアプリの作り込みは完了した。

## html ファイルの作り込み

最後に、html ファイルの作り込みを行う。  

`accounts` アプリで必要となるファイルは以下の 3 つ。  

 - templates/accounts/form.html  
```html
{% extends "base.html" %}
{% load django_bootstrap5 %}

{# ユーザーがログインしているかどうかは、`user.is_authenticated` で判定できる #}
{# https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User.is_authenticated #}
{% block title %}ユーザー{% if user.is_authenticated %}の追加{% else %}登録{% endif %}{% endblock title %}

{% block content %}
<h4 class="mt-4 mb-5 border-bottom">ユーザー{% if user.is_authenticated %}の追加{% else %}登録{% endif %}</h4>

<form method="post">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ next }}" />
    {% bootstrap_form form %}
    <div class="form-group row">
        <div class="offset-md-3 col-md-9">
          <button type="submit" class="btn btn-primary">{% if user.is_authenticated %}追加{% else %}登録{% endif %}</button>
        </div>
      </div>
</form>
{% endblock %}
```
 - templates/accounts/list.html  
```html
{% extends "base.html" %}

{% block title %}ユーザーの一覧{% endblock title %}

{% block content %}
    <h4 class="mt-4 border-bottom">ユーザーの一覧</h4>
    <a href="{% url 'accounts:create' %}" class="btn btn-primary btn-sm my-3">追加</a>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {% for account in object_list %}
        <tr>
          <th scope="row">{{ account.id }}</th>
          <td>{{ account.username }}</td>
          <td>
            {% if account.is_superuser %}{# スーパーユーザーの場合 #}
            <button type="button" class="btn btn-outline-secondary btn-sm" title="スーパーユーザーは削除できません。">削除</button>
            {% else %}{# スーパーユーザー以外の場合 #}
            <a href="javascript:void(0)" data-id="{{ account.id }}" data-delete_confirmation_message="ユーザー {{ account.username }} を削除しますか？" class="btn btn-outline-primary btn-sm delete-btn">削除</a>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    <!-- 削除を確認するモーダルダイアログ -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">削除確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p id="delete-confirmation-message"></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
            <button type="button" class="btn btn-primary" id="deletion-submitted">削除</button>
          </div>
        </div>
      </div>
    </div>
{% endblock content %}
{% block scripts %}
<script>
  $(document).ready(()=>{

    // レコードの削除
    $('.delete-btn').on('click', function(){ // 削除ボタンクリック時

      $('#delete-confirmation-message').text(this.dataset.delete_confirmation_message);
      $('#deleteModal').modal('show');
      $('#deletion-submitted').off('click'); // 重複して登録しないように、'click' イベントが存在する場合は削除
      $('#deletion-submitted').on('click', null, this.dataset.id, function(obj_event){
        $('#deleteModal').modal('hide');

        // 削除用 URL を POST で叩く
        $.ajax({
          url: '/accounts/' + obj_event.data + '/delete/',
          method: 'POST',
          headers: {'X-CSRFToken': dict_utilities.getValueFromCookie('csrftoken')},
        }).done(() =>{
          location.reload();
        });

      });
    });
  });
</script>
{% endblock scripts %}
```
 - templates/accounts/login.html  
```html
{% extends "base.html" %}
{% load django_bootstrap5 %}

{% block title %}ログイン{% endblock title %}

{% block content %}
<h4 class="mt-4 mb-5 border-bottom">ログイン</h4>

<form method="post">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ next }}" />
    {% bootstrap_form form %}
    <div class="form-group row">
        <div class="offset-md-3 col-md-9">
          <button type="submit" class="btn btn-primary">ログイン</button>
        </div>
      </div>
</form>
{% endblock %}
```
`index` アプリで必要となる html ファイルは以下 1 つのみとする。  
この章では、まずはメインページの表示ができることだけを確認したいので、ひとまず以下のみとしている。  
以降の章で、詳細な定義を作り込んでいく。  

 - templates/index/index.html
```html
{% extends "base.html" %}

{% block content %}
    <div class="welcome">
      <h4 class="title">Main Page</h4>
      <p class="subtitle">subtitle</p>
    </div>
{% endblock %}
```

最後に、編集者の一覧やログインページにジャンプすることができるナビバーを templates/base.html に作り込んでいく。  

 - templates/base.html  
```html
{% load i18n static %}
<!DOCTYPE html>{% get_current_language as LANGUAGE_CODE %}
<html lang="{{ LANGUAGE_CODE|default:"en-us" }}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
{% block extra_css %}{% endblock %}
<title>{% block title %}My books{% endblock %}</title>
</head>
<body>
  <nav class="navbar navbar-expand flex-md-row navbar-dark bg-dark">
    <div class="container justify-content-between">
      <a href="/" class="navbar-brand">書籍ライブラリ</a>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {# ドロップダウンの実装方法は右参照 https://getbootstrap.jp/docs/5.0/components/navbar/#nav #}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuBooks" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            書籍
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuBooks">
            <li><a class="dropdown-item" href="/">書籍の一覧</a></li>
            <li><a class="dropdown-item" href="{% url 'editors:list' %}">編集者の一覧</a></li>
          </ul>
        </li>
      </ul>
      <ul class="navbar-nav mr-md-2">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuAccounts" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            {# ユーザーがログインしているかどうかは、`user.is_authenticated` で判定できる #}
            {# https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User.is_authenticated #}
            {% if user.is_authenticated %}
            {# ユーザー名は、`user.username` で取得できる #}
            {# https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User.username #}
            {{ user.username }}
            {% else %}
            ログアウト中
            {% endif %}
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuAccounts">
            <li>
              <a class="dropdown-item" href="{% url 'accounts:list' %}">ユーザーの一覧</a>
            </li>
            {% if user.is_authenticated %}
            <li>
              <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#logoutModal">ログアウト</button>
            </li>
            {% endif %}
          </ul>
        </li>
        {% if not user.is_authenticated %}
        <li class="nav-item"><a class="nav-link" href="{% url 'accounts:signup' %}">ユーザー登録</a></li>
        {% endif %}
      </ul>
    </div>
  </nav>
  <!-- ログアウトを確認するモーダルダイアログ -->
  <div class="modal fade" id="logoutModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">ログアウト確認</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>ログアウトしますか？</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
          <a class="btn btn-primary" href="{% url 'accounts:logout' %}" role="button">ログアウト</a> {# `<a>` タグをボタンの見た目にする方法は右参照 https://getbootstrap.jp/docs/5.0/components/buttons/#button-tags #}
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    {% block content %}
      {{ content }}
    {% endblock %}
  </div>
<script src="{% static 'js/jquery-3.6.0.min.js' %}"></script>
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
<script src="{% static 'js/utility.js' %}"></script>
{% block scripts %}
  {{ scripts }}
{% endblock %}
</body>
</html>
```

## 動作確認

`python manage.py runserver` して、ブラウザで `http://127.0.0.1:8000/` にアクセスすれば、`http://127.0.0.1:8000/accounts/login/` にリダイレクトされてログインページが表示される。 
ユーザー名、パスワードは、`# 環境のセットアップ・PJ の作成` 時の `# ユーザーの作成` で作成したユーザー名 `admin`、パスワード `administrator1` を使用すればいい。  

![](assets/images/2022-04-03-18-03-13.png)  

ログインすればメインページが表示 (かなり簡素だが) され、  

![](assets/images/2022-04-03-18-05-32.png)  

画面右上のユーザー名をクリックして現れるドロップダウンメニューから `ユーザーの一覧` を選択すればユーザーの一覧画面に遷移する。  

![](assets/images/user-list-01.svg)  

`追加` ボタンをクリックすればユーザーの追加画面に遷移し、  

![](assets/images/2022-04-03-18-19-31.png)  

新たなユーザーが登録できる。  

![](assets/images/2022-04-03-18-21-04.png)  

ナビバーの (ユーザー名) -> `ログアウト` でログアウトすれば、`http://127.0.0.1:8000/accounts/login/` にリダイレクトされる。この画面のナビバー右側 `ユーザー登録` をクリックすれば新規ユーザーを登録できる。  

![](assets/images/2022-04-03-18-24-02.png)  

また、ログイン状態でナビバー `書籍` -> `編集者の一覧` をクリックすれば、前章まで アクセスしていた `http://127.0.0.1:8000/editors/` に行くことができる。

![](assets/images/editors-list-01.svg)  

## ここまでのソースコード

この項で実装したソースコードを、example/07-user-auth/main に置いた。  

# REST API

外部アプリとの連携に必要となる、REST API の実装をしよう。  
そのために、まずこの Web アプリにアクセスするための認証トークンを発行、管理する仕組みから実装していく。  
Django REST framework というパッケージを利用して、ユーザーに紐づくトークンを管理する機能を実装しよう。  

`# 環境のセットアップ・PJ の作成` の章で実施したように、Django REST framework はインストール済みなので、アプリケーションの登録から行っていく。  

## (認証トークン管理) アプリケーションの登録

これまでと同じく、main/settings.py に以下のように追記する

 - main/settings.py  
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5', # テンプレートファイル内で `{% load django_bootstrap5 %}` するなら左記のように追記
    'widget_tweaks', # テンプレートファイル内で `{% load widget_tweaks %}` するなら左記のように追記
    'rest_framework', # Django REST framework の機能を使う場合は左記のように追記 # <- ここを追加
    'editors', # `~python.exe manage.py startapp xxx` で作成したアプリ名
    'accounts',
    'index',
]
```

## (認証トークン管理) URL スキームの設計

各ユーザーに紐づくトークンを作成、削除する機能を実装したいので、URL スキームは以下の様にする。

 - accounts/urls.py  
```python
urlpatterns = [
    path('signup/', CreateView.as_view(
        template_name = 'accounts/form.html',
        form_class = UserCreationForm,
        success_url = '/',
    ), name='signup'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user = True,
        # note
        # ログインページにアクセスする認証済みユーザーが、ログインに成功したかのようにリダイレクトさせる。
        # https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.views.LoginView.redirect_authenticated_user
        
        template_name = 'accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('', views.AccountsListView.as_view(), name = 'list'), # Read
    path('<int:pk>/delete/', views.AccountDelete.as_view(), name = 'delete'),
    path('<int:pk>/token/create/', views.createToken, name = 'create_token'), # <- ここを追加
    path('<int:pk>/token/delete/', views.deleteToken, name = 'delete_token'), # <- ここを追加
]
```

## (認証トークン管理) モデル定義・フィールド定義

認証トークンのモデル定義は、`rest_framework.authtoken.models.Token` を継承する形で、以下の様にして実装できる。

 - accounts/models.py
```python
class TokenForRESTAPI(Token):
    
    expired_date = models.DateTimeField(verbose_name = '有効期限', null = True, blank = True)

    class Expiration(StrChoiceEnum):
        ONE_WEEK = ('7 days', '1 週間')
        ONE_MONTH = ('30 days', '1 ヶ月間')
        THREE_MONTHS = ('90 days', '3 ヶ月間')
        NO_EXPIRATION = ('no expiration', '有効期限なし')

    expiration = models.CharField(verbose_name = '設定有効期限', max_length = 16, choices = Expiration.choices(), null = True)
```

## (認証トークン管理) View 定義

Django REST framework の機能で、ユーザーに紐づくトークンは、そのモデル内の外部参照キーのフィールド `auth_token` が定義されている。その為、html 側のユーザー一覧のリストからこのトークンにアクセスできるよう accounts/views.py の `class AccountCreateView(CreateView):` を以下の様に変更しよう。  

 - 変更前  
```python
class AccountCreateView(CreateView):
    model = User
    template_name = 'accounts/form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:list')
```
 - 変更後  
```python
class AccountsListView(ListView):
    model = User
    
    queryset = User.objects.prefetch_related('auth_token')
    #
    # note1
    # `queryset`
    # View 関数がテンプレートに返すオブジェクトリスト。指定されていない場合は、`model = ` に指定したモデルの `.objects.a()` が指定される。
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectMixin.model
    #
    # note2
    # `.prefetch_related('auth_token')`
    # django-rest-framework が提供する rest_framework.authtoken.models.Token モデルが User を外部キーとして参照している。  
    # その為、User から Token モデルを参照(逆参照)するため `prefetch_related` で取得している。  
    # https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/models.py



    template_name = 'accounts/list.html'
    success_url = reverse_lazy('accounts:list')
```
さらに、トークン作成、削除に関する View 関数を以下のように追加しよう。
```python
def createToken(request, pk):

    obj_user = get_object_or_404(User, id = pk)
    # note
    # `get_object_or_404`
    # オブジェクトを検索し、存在しない場合は `Http404` を Raise する
    # https://docs.djangoproject.com/ja/2.2/topics/http/shortcuts/#django.shortcuts.get_object_or_404
    
    if request.method == 'POST':
        
        obj_form = TokenEditForm(request.POST)
        
        if obj_form.is_valid():

            TokenForRESTAPI.objects.filter(user = obj_user).delete() # 既存のトークンを削除

            obj_token = obj_form.save(commit = False) # データベースに保存する前のモデルインスタンスを取得

            # 有効期限の設定
            if obj_token.expiration == TokenForRESTAPI.Expiration.ONE_WEEK:
                obj_token.expired_date = datetime.datetime.now() + datetime.timedelta(days = 7) # 7 日加算
            elif obj_token.expiration == TokenForRESTAPI.Expiration.ONE_MONTH:
                obj_token.expired_date = datetime.datetime.now() + relativedelta(months = 1) # 1 ヶ月加算
            elif obj_token.expiration == TokenForRESTAPI.Expiration.THREE_MONTHS:
                obj_token.expired_date = datetime.datetime.now() + relativedelta(months = 3) # 3 ヶ月加算
            else:
                obj_token.expired_date = None

            obj_token.user = obj_user # ユーザーの設定

            obj_token.save()

            return JsonResponse({'token': obj_token.key})

    else: # request method が GET の場合
        obj_form = TokenEditForm()
    
    # form が invalid もしくは request method が GET の場合
    return render(request, "accounts/form_token.html", {'form': obj_form})

def deleteToken(request, pk):

    obj_user = get_object_or_404(User, id = pk)

    TokenForRESTAPI.objects.filter(user = obj_user).delete()

    return redirect('accounts:list')
```
ここで必要になるフォーム `TokenEditForm` は accounts/forms.py を新たに定義して内容を以下のようにする。  

 - accounts/forms.py  
```python
from django import forms

from .models import TokenForRESTAPI

class TokenEditForm(forms.ModelForm):

    # モデル定義で `null = True`` とすると、そのフィールドのドロップダウンメニューに `--------` が追加されてしまう。  
    # フォーム上の入力は TokenForRESTAPI.Expiration.choices() のリスト内からいずれかを必須で選択する仕組みにしたいので、  
    # 以下のようにしてオーバーライドして定義する。  
    expiration = forms.ChoiceField(
        label = '設定有効期限',
        choices = TokenForRESTAPI.Expiration.choices(),
        initial = TokenForRESTAPI.Expiration.ONE_MONTH.value,
    )

    class Meta:
        model = TokenForRESTAPI
        fields = (
            'expiration',
        )
```

## (認証トークン管理) html ファイルの作り込み

ユーザー一覧に関する html ファイル accounts/list.html 、トークン生成に関する html ファイル accounts/form_token.html をそれぞれ以下の様に定義していく。  

 - accounts/list.html  
```html
{% extends "base.html" %}

{% block title %}ユーザーの一覧{% endblock title %}

{% block content %}
    <h4 class="mt-4 border-bottom">ユーザーの一覧</h4>
    <a href="{% url 'accounts:create' %}" class="btn btn-primary btn-sm my-3">追加</a>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">名前</th>
          <th scope="col">トークン</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        {% for account in object_list %}
        <tr>
          <th scope="row">{{ account.id }}</th>
          <td>{{ account.username }}</td>
          <td>
            {% if account.auth_token.key %}{# トークンが存在する場合 #}
            
            {{ account.auth_token.key|slice:":6" }}---------------------------------- トークン有効期限 : {% if account.auth_token.expired_date %}{{ account.auth_token.expired_date }}{% else %}有効期限なし{% endif %}
            {# `slice` の意味は右参照 https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#slice #}

            {% else %}{# トークンが存在しない場合 #}
            トークン未生成
            {% endif %}
          </td>
          <td>
            {% if account.auth_token.key %}{# トークンが存在する場合 #}
            <button type="button" class="btn btn-outline-secondary btn-sm" title="トークンは生成済みです。">トークンの生成</button>
            <a href="javascript:void(0)" data-deletion_url="/accounts/{{ account.id }}/token/delete/" data-delete_confirmation_message="{{ account.username }} のトークンを削除しますか？" class="btn btn-outline-primary btn-sm delete-btn">トークンの削除</a>
            {% else %}{# トークンが存在しない場合 #}
            <a href="{% url 'accounts:create_token' pk=account.id %}" class="btn btn-outline-primary btn-sm">トークンの生成</a>
            <button type="button" class="btn btn-outline-secondary btn-sm" title="トークンは未生成です。">トークンの削除</button>
            {% endif %}
            {% if account.is_superuser %}{# スーパーユーザーの場合 #}
            <button type="button" class="btn btn-outline-secondary btn-sm" title="スーパーユーザーは削除できません。">ユーザーの削除</button>
            {% else %}{# スーパーユーザー以外の場合 #}
            <a href="javascript:void(0)" data-deletion_url="/accounts/{{ account.id }}/delete/" data-delete_confirmation_message="ユーザー {{ account.username }} を削除しますか？" class="btn btn-outline-primary btn-sm delete-btn">ユーザーの削除</a>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    <!-- 削除を確認するモーダルダイアログ -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">削除確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p id="delete-confirmation-message"></p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
            <button type="button" class="btn btn-primary" id="deletion-submitted">削除</button>
          </div>
        </div>
      </div>
    </div>
{% endblock content %}
{% block scripts %}
<script>
  $(document).ready(()=>{

    // トークンの生成
    $('.token-creation-btn').on('click', function(){ // トークン生成ボタンクリック時
      $('#delete-confirmation-message').text(this.dataset.token_creation_message);
    });

    // レコードの削除
    $('.delete-btn').on('click', function(){ // 削除ボタンクリック時

      $('#delete-confirmation-message').text(this.dataset.delete_confirmation_message);
      $('#deleteModal').modal('show');
      $('#deletion-submitted').off('click'); // 重複して登録しないように、'click' イベントが存在する場合は削除
      $('#deletion-submitted').on('click', null, this.dataset.deletion_url, function(obj_event){
        $('#deleteModal').modal('hide');

        // 削除用 URL を POST で叩く
        $.ajax({
          url: obj_event.data,
          method: 'POST',
          headers: {'X-CSRFToken': dict_utilities.getValueFromCookie('csrftoken')},
        }).done(() =>{
          location.reload();
        });

      });
    });
  });
</script>
{% endblock scripts %}
```
 - accounts/form_token.html
```html
{% extends "base.html" %}
{% load django_bootstrap5 %}

{% block title %}トークンの生成{% endblock title %}

{% block content %}
    <h4 class="mt-4 mb-5 border-bottom">トークンの生成</h4>
    <form method="post">
      {% csrf_token %}

      {% include "form.html" with obj_field=form.expiration str_help_message="有効期限を設定します。"%}
      
      <div class="form-group row">
        <div class="offset-md-3 col-md-9">
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#tokenCreateConfirmationModal">
            生成
          </button>
        </div>
      </div>
    </form>
    <a href="{% url 'accounts:list' %}" class="btn btn-secondary btn-sm">戻る</a>

    <!-- トークン生成を確認するモーダルダイアログ -->
    <div class="modal fade" id="tokenCreateConfirmationModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">トークンの生成確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>トークンを生成します。次のダイアログ以降トークン文字列を確認することはできません。</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
            <a href="javascript:void(0)" id="tokenCreateConfirmation" class="btn btn-primary">生成</a>
          </div>
        </div>
      </div>
    </div>
    <!-- 生成されたトークン表示するモーダルダイアログ -->
    <div class="modal fade" id="tokenCreatedModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">生成トークンの確認</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>トークンを生成しました。</p>
            <p id="tokenCreatedParagraph"></p>
          </div>
          <div class="modal-footer">
            <a href="/accounts" class="btn btn-primary">確認</a>
          </div>
        </div>
      </div>
    </div>
{% endblock content %}
{% block scripts %}
<script>
  $(document).ready(()=>{

    // トークンの生成
    $('#tokenCreateConfirmation').on('click', function(){
      $('#tokenCreateConfirmationModal').modal('hide');

      // トークン生成 URL を POST で叩く
      $.ajax({
        url: location.pathname, // 現在のパス
        method: 'POST',
        headers: {'X-CSRFToken': dict_utilities.getValueFromCookie('csrftoken')},
        data: {expiration: document.getElementById('id_expiration').value},
      }).done((dict_data) =>{
        // 生成されたトークンを表示
        $('#tokenCreatedParagraph').text(dict_data.token);
        $('#tokenCreatedModal').modal('show');
      });

    });

    // CSV 入力
    $('#csv-input-btn').on('click', function(){ // CSV 入力ボタンクリック時
      $('#CSVInputModal').modal('show');
    });
  });
</script>
{% endblock scripts %}
```

## (認証トークン管理) 動作確認

accounts アプリのモデル定義を変更したので、以下を実施してから `python manage.py runserver` しよう。  
 - `python manage.py makemigrations`  
 - `python manage.py migrate`  

ユーザー一覧でトークンの生成、トークンの削除ボタンが定義されているはずだ。  

![](assets/images/2022-04-07-21-00-51.png)  

トークンの生成ボタンをクリックすれば、トークンの生成画面に遷移し、  

![](assets/images/2022-04-07-21-02-49.png)  

生成ボタンをクリックすれば生成確認ダイアログが表示される。  

![](assets/images/2022-04-07-21-03-55.png)  

ここでさらに生成ボタンをクリックすると、生成されたトークンが確認できる。  

![](assets/images/2022-04-07-21-05-46.png)  

ユーザー一覧画面に戻ると、生成されたトークンの先頭 6 文字のみと有効期限が表示される。  

![](assets/images/2022-04-07-21-07-55.png)  

あとは、この認証トークンを使ってアクセスされた際の動きを定義していく。

## URL スキームの設計

新しいアプリを作成したわけではないが、REST API にかかわる URL 定義は `api/v1/` から始まる定義だ。という風に、定義付けしておくのが良い。main/urls.py に以下のように定義を追加する。  

 - main/urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),

    # note
    # 第1引数には ``<`~python.exe manage.py startapp xxx` で作成したアプリ名>/`` を指定
    # 第2引数には ``include('<`~python.exe manage.py startapp xxx` で作成したアプリ名>.urls')`` を指定
    path('editors/', include('editors.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('index.urls')),
    # URL で API のメジャーバージョンが指定できるように、`v1/` を URL に追加
    path('api/v1/', include('common.apiv1_urls')), # <- ここを追加
]
```
そして、 common/apiv1_urls.py という新しいファイルを作成し、内容を以下のようにする。  

 - common/apiv1_urls.py
```python
from django.urls import path
from django.views.decorators.http import require_http_methods

import editors.views

app_name = 'apiv1'

urlpatterns = [
    path('editors/create/', require_http_methods(['POST'])(editors.views.EditorCreateAPIView.as_view()), name = 'editor_create'),
    path('editors.json/', require_http_methods(['HEAD', 'GET'])(editors.views.EditorListAPIView.as_view()), name = 'editors_list'),
    path('editors/update/', require_http_methods(['POST'])(editors.views.EditorUpdateAPIView.as_view()), name = 'editor_update'),
    path('editors/<int:pk>/delete/', require_http_methods(['DELETE'])(editors.views.EditorDeleteAPIView.as_view()), name = 'editor_delete'),
]
```

また、REST API はトークン認証でアクセスする方式をとるので、上記 `api/` から始まる URL は通常のユーザーログイン確認対象から外したい。その為、main/settings.py に以下のように定義を追加する。  

 - main/settings.py  
```python
# ログインが不要な URL 文字列の正規表現一覧
STR_URL_EXCEPTION_THAT_REQUIRES_LOGIN = [
    r'/accounts/login/(.*)$',
    r'/accounts/signup/(.*)$',
    r'/api/(.*)$',
]
```

## モデル定義・フィールド定義

REST API については、単なる API であるので、新たなモデル定義は必要ない。  

## View 定義

"View 定義" といってよいのかどうかわからないが、REST API における View 定義は以下の 3 つで構成される。  

 - トークン認証機能  
 - 指定されたデータを検証するシリアライズ機能(通常の View 定義におけるフォームに相当する)  
 - 実行命令を受け取る、実行結果を返す機能  

一つずつ実装していこう。  

### トークン認証機能

common/auth.py というファイルを新たに定義して、内容を以下のようにする。  

 - common/auth.py  
```python
import logging

from django.utils import timezone

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.const import STR_ATTRIBUTE_KEYWORD_FOR_TOKEN

from accounts.models import TokenForRESTAPI

logger = logging.getLogger(__name__)

class TokenAuthenticationForRESTAPI(TokenAuthentication):
# note
# `TokenAuthentication`
# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
# -> `class TokenAuthentication(BaseAuthentication):`

    keyword = STR_ATTRIBUTE_KEYWORD_FOR_TOKEN
    model = TokenForRESTAPI

    def authenticate(self, request):
        """
        認証トークンの期限切れチェックを行う。
        """
        # note
        # 以下をオーバーライドしている。  
        # https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py  
        # -> `class TokenAuthentication(BaseAuthentication):`  
        #   -> `def authenticate(self, request):`  
        
        # オーバーライド元の `def authenticate(self, request):` を実行。  
        # 認証を通過した場合は、返却値として `(token.user, token)` が返ってくる。
        obj_resultOfAuthentication = super().authenticate(request)

        # 認証に通過した場合は、`def authenticate(self, request):` の返却値が `(token.user, token)` となるが、  
        # 認証に失敗した場合は rest_framework.exceptions.AuthenticationFailed が raise されるので、返却値が None となる
        if obj_resultOfAuthentication: # 認証に通過した場合
            
            _, obj_token = obj_resultOfAuthentication

            if obj_token.expired_date and obj_token.expired_date < timezone.localtime():
                logger.warning('The authentication token has expired.')
                raise AuthenticationFailed('認証トークンの期限切れです。')

        return obj_resultOfAuthentication

class TokenAPIView(APIView):
    """
    トークン認証クラス
    """
    # note
    # APIView の実装方法は以下を参照  
    # https://www.django-rest-framework.org/api-guide/views/#class-based-views

    authentication_classes = [TokenAuthenticationForRESTAPI]
    permission_classes = [IsAuthenticated]


    def finalize_response(self, request, response, *args, **kwargs):
        """
        トークン認証が通過なかった場合に、Warning ログを出力する
        """
        #
        # note1
        # View 関数の終了時にコールされる。  
        # 以下をオーバーライドしている。  
        # https://www.django-rest-framework.org/api-guide/views/#finalize_responseself-request-response-args-kwargs
        # -> `.finalize_response(self, request, response, *args, **kwargs)`  
        #
        # note2
        # https://www.django-rest-framework.org/api-guide/views/#finalize_responseself-request-response-args-kwargs
        # -> `.initialize_request(self, request, *args, **kwargs)`
        # 上記関数は `authentication_classes`, `permission_classes` の実行前にコールされる。 
        # この段階では、`request.user.is_authenticated` の正しい値が取得できないので、
        # `def finalize_response(self, request, response, *args, **kwargs):` 内で評価する
        
        if not request.user.is_authenticated: # トークン認証が通過なかった場合
            logger.warning(f'Token authentication faild. status:{response.status_code}')

        return super().finalize_response(request, response, *args, **kwargs)
```
上記で新たに定義した `STR_ATTRIBUTE_KEYWORD_FOR_TOKEN` を、common/const.py に以下のように追加する。  

 - common/const.py
```python
#
# REST API でトークン認証するためトークンに対応する属性名
# e.g.
# `curl --header "authorization: Token 512ebc85cd4a1a1a5325a2d6203cecf65b5d94eb"`
#                                ↑
#                                この部分のことを指す
STR_ATTRIBUTE_KEYWORD_FOR_TOKEN = 'Token'
```

### シリアライズ機能

editors/serializer.py というファイルを新たに定義して、内容を以下のようにする。  

 - editors/serializer.py
```python
from django.db.models import Q

from rest_framework import serializers

from .models import Editor

#
# `~restapi/editors.json?id=1&name=admin` のようにクエリ文字列 (クエリストリング) が付与されていた場合に、  
# そのパラメータについてバリデーションをかけるクラス  
# `instance = EditorSerializerForQueryString(data = request.GET)` のようにしてインスタンス化する。  
# インスタンス化して `.is_valid()` がコールされた際にバリデーションが行われ、  
# `self.validated_data` にバリデーションに通過した値が入る。  
# `~restapi/editors.json?foo=1&bar=admin` のように不明なクエリ文字列が指定されていた場合は、  
# そのフィールドは無視する。  
class EditorSerializerForQueryString(serializers.Serializer):

    id = serializers.IntegerField(required = False)
    name = serializers.CharField(required = False)

    # note
    # `def create(self, validated_data):`, `def update(self, instance, validated_data):`
    # https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-serializer-class
    # インスタンス化したこのクラスの `.save()` method がコールされた際に呼ばれる。  
    # このクラスの用途は、クエリ文字列に対してバリデーションをかけることだけなので、  
    # `.save()` method がコールされることは考慮しない。
    # その為、以下関数は両方ともなにもせずに None を返すこととする。
    # (これらの関数がコールされること自体が運用上無い想定)  
    def create(self, validated_data):
        return None
    def update(self, instance, validated_data):
        return None

    def getQueryDictForFilter(self):
        dict_queryForFilter = {}

        for str_fieldName in ['id','name']:
            if self.validated_data.get(str_fieldName):
                dict_queryForFilter[str_fieldName] = self.validated_data.get(str_fieldName)
        
        return dict_queryForFilter

class EditorSerializerForCreate(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 255)
    sex = serializers.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False, allow_blank = True)

    class Meta:
        model = Editor
        fields = (
            'name',
            'sex',
        )

    # note
    # 以下を参考にバリデーション機能を定義
    # https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    def validate(self, data):

        if Editor.objects.filter(name = data.get('name')).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Editor が既に存在します。')
            # note
            # このフィールドの重複チェックは、ここで行わなくても、もし重複があった場合は、  
            # common/views.py -> `class TokenAPIViewForCreation(TokenAPIView):` -> `serializer.save()` の時に  
            # `IntegrityError` が発生するが、エラーメッセージの文言が
            # 「UNIQUE constraint failed: editors_editor.name」 とわかりにくい為、
            # ここで重複時のエラーメッセージを生成している
        
        tmp_sex = data.get('sex')
        if tmp_sex:
            data['sex'] = dict(self.fields['sex'].choices).get(tmp_sex)
        else:
            data['sex'] = None

        return data

class EditorSerializerForUpdate(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 255)
    sex = serializers.ChoiceField(choices = Editor.Sex.reversedChoices(), required = False, allow_blank = True)

    class Meta:
        model = Editor
        fields = '__all__'

    def validate(self, data):

        # 別レコードですでに使われている名前かどうかチェック
        if Editor.objects.filter(
            ~Q(id = data.get('id')) &
            Q(name = data.get('name'))
        ).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Editor が既に存在します。')
        
        tmp_sex = data.get('sex')
        if tmp_sex:
            data['sex'] = dict(self.fields['sex'].choices).get(tmp_sex)
        else:
            data['sex'] = None

        return data
```

### 実行命令を受け取る、実行結果を返す機能

`### トークン認証機能` の common/auth.py で実装した、`class TokenAPIView(APIView):` を拡張して、POST, GET, DELETE 時の共通処理を、common/views.py を新たに定義して以下の内容にする。  

 - common/views.py  
```python
import json
import logging

from django.db import transaction
from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from common.utilities import getQeryStringInURL

from .auth import TokenAPIView

logger = logging.getLogger(__name__)

class TokenAPIViewForCreation(TokenAPIView):
    """
    トークン認証クラス `TokenAPIView` を拡張した POST 時共通処理定義クラス
    """
    property_keyword = ''
    serializer = None
    
    def post(self, request, *args, **kwargs):
        # note  
        # POST メソッドでアクセスされた際にコールされる。  
        # https://docs.djangoproject.com/en/4.0/ref/class-based-views/base/#django.views.generic.base.View.dispatch  
        # `def post(self, request, *args, **kwargs):` という風に定義しているのは、以下を参考にした為  
        # https://docs.djangoproject.com/en/4.0/ref/class-based-views/base/#view  
        
        # JSON ファイルのパース
        try:
            dict_specifiedData = json.loads(request.body)

        except json.JSONDecodeError as err: # JSON フォーマットになっていない場合
            str_errmsg = f'JSONDecodeError occured while `json.loads`. Check following.\nError message: {str(err)}\nrequest.body: {request.body}'
            logger.warning(str_errmsg)
            return Response({'detail': str_errmsg}, status=status.HTTP_400_BAD_REQUEST)

        # パースしたデータが辞書型でないもしくはあらかじめ定めておいたプロパティ名で定義された値が list でない場合
        if (not isinstance(dict_specifiedData, dict)) or (not isinstance(dict_specifiedData.get(self.property_keyword), list)):
            str_errmsg = (f'Unexpected format: {request.body}')
            logger.warning(str_errmsg)
            return Response({'detail': str_errmsg}, status=status.HTTP_400_BAD_REQUEST)

        str_errmsg = ''
        try:
            with transaction.atomic():
                
                # レコード登録ループ
                for dict_toSerialize in dict_specifiedData[self.property_keyword]:
                    serializer = self.serializer(data = dict_toSerialize)
                    # note
                    # 新規作成の場合は、上記のように、`(data = ~` に保存するレコードをディクショナリ型で指定する

                    if serializer.is_valid(): # バリデーションの実行
                        serializer.save()

                    else: # バリデーション NG の場合
                        str_errmsg = f'Validation error: {serializer.errors}'
                        logger.warning(str_errmsg)
                        raise ValueError(str_errmsg)

        except ValueError as err: # バリデーション NG のレコードがある場合
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

        except OperationalError as err:
            # デッドロックの可能性。
            str_errmsg = f'There is a possibility of deadlock. Check following.\n{str(err)}'
            logger.error(str_errmsg)
            return Response({'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({}, status=status.HTTP_200_OK)

class TokenAPIViewForList(TokenAPIView):
    """
    トークン認証クラス `TokenAPIView` を拡張した GET 時共通処理定義クラス
    """
    model = None
    property_keyword = ''
    serializer = None
    dictionarizer = None

    # GET メソッドでアクセスされた際にコールされる。
    def get(self, request, *args, **kwargs):

        # クエリ文字列 (クエリストリング) のバリデーション
        obj_serializer = self.serializer(data = request.GET)

        if obj_serializer.is_valid(): # クエリ文字列のバリデーション OK の場合

            # クエリ文字列で指定されたパラメーターでフィルタ (指定がない場合は全レコード対象) して辞書配列化
            obj_editors = self.model.objects.filter(**obj_serializer.getQueryDictForFilter()).order_by('id')
            dict_editors = self.dictionarizer(obj_editors)

        else: # クエリ文字列のバリデーションエラーの場合
            str_errmsg = f'Validation error found in {request.path}{getQeryStringInURL(request.GET)}'
            logger.warning(str_errmsg)
            return Response({'detail': str_errmsg}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            self.property_keyword: dict_editors
        })

class TokenAPIViewForUpdate(TokenAPIView):
    """
    トークン認証クラス `TokenAPIView` を拡張した UPDATE (POST) 時共通処理定義クラス
    """
    model = None
    property_keyword = ''
    serializer = None
    
    # POST メソッドでアクセスされた際にコールされる。
    def post(self, request, *args, **kwargs):
        
        # JSON ファイルのパース
        try:
            dict_specifiedData = json.loads(request.body)

        except json.JSONDecodeError as err: # JSON フォーマットになっていない場合
            str_errmsg = f'JSONDecodeError occured while `json.loads`. Check following.\nError message: {str(err)}\nrequest.body: {request.body}'
            logger.warning(str_errmsg)
            return Response({'detail': str_errmsg}, status=status.HTTP_400_BAD_REQUEST)

        # パースしたデータが辞書型でないもしくはあらかじめ定めておいたプロパティ名で定義された値が list でない場合
        if (not isinstance(dict_specifiedData, dict)) or (not isinstance(dict_specifiedData.get(self.property_keyword), list)):
            str_errmsg = (f'Unexpected format: {request.body}')
            logger.warning(str_errmsg)
            return Response({'detail': str_errmsg}, status=status.HTTP_400_BAD_REQUEST)

        str_errmsg = ''
        try:
            with transaction.atomic():

                # レコード登録ループ
                for dict_toSerialize in dict_specifiedData[self.property_keyword]:
                    
                    if not dict_toSerialize.get('id'): # `id` プロパティが存在しない場合
                        str_errmsg = f'Validation error: property `id` not found in "{json.dumps(dict_toSerialize)}"'
                        logger.warning(str_errmsg)
                        raise ValueError(str_errmsg)

                    obj_model = get_object_or_404(self.model, id = dict_toSerialize['id'])
                    serializer = self.serializer(instance = obj_model, data = dict_toSerialize)
                    # note  
                    # 更新の場合は、上記のように、`(instance = ~` 更新対象のオブジェクトを指定する  
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        str_errmsg = f'Validation error: {serializer.errors}'
                        logger.warning(str_errmsg)
                        raise ValueError(str_errmsg)

        except ValueError as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

        except OperationalError as err:
            # デッドロックの可能性。
            str_errmsg = f'There is a possibility of deadlock. Check following.\n{str(err)}'
            logger.error(str_errmsg)
            return Response({'detail': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({})

class TokenAPIViewForDeletion(TokenAPIView):
    """
    トークン認証クラス `TokenAPIView` を拡張した DELETE 時共通処理定義クラス
    """
    model = None

    # DELETE メソッドでアクセスされた際にコールされる。
    def delete(self, request, pk, *args, **kwargs):
        
        obj_queryset = self.model.objects.filter(id = pk)
        
        if obj_queryset: # 削除対象オブジェクトが存在する場合
            obj_queryset.delete()
            return Response({}, status=status.HTTP_200_OK)
        
        # 削除対象オブジェクトが存在しない場合
        str_errmsg = f'Specified Editor ID: {pk} not found.'
        logger.warning(str_errmsg)
        return Response({'detail': str_errmsg}, status=status.HTTP_404_NOT_FOUND)
```
ここで、`class TokenAPIViewForList(TokenAPIView):` 内の `str_errmsg = f'Validation error found in {request.path}{getQeryStringInURL(request.GET)}'` に必要な関数 (ディクショナリ化されたクエリ文字列を元に戻す関数) `getQeryStringInURL` を common/utilities.py に定義する。  

 - common/utilities.py
```python
def getQeryStringInURL(dict_params):
    """
    ディクショナリ化されたクエリ文字列 (クエリストリング) を元に戻す
    """
    str_queryStringInURL = ''

    if dict_params: # クエリ文字列が指定されていた場合
        str_queryStrings = []
        for str_key, var_val in dict_params.items():
            str_queryStrings.append(str_key + '=' + urllib.parse.quote(str(var_val)))
        str_queryStringInURL = '?' + '&'.join(str_queryStrings)

    return str_queryStringInURL
```

これで、POST, GET, DELETE 時の共通処理は整ったので、あとは editors/views.py に追加、読み込み、更新、削除時の処理を定義していく。  

 - editors/views.py
```python
class EditorCreateAPIView(TokenAPIViewForCreation):
    property_keyword = 'editors'
    serializer = EditorSerializerForCreate

class EditorListAPIView(TokenAPIViewForList):
    model = Editor
    property_keyword = 'editors'
    serializer = EditorSerializerForQueryString
    dictionarizer = makeDictFromEditors

class EditorUpdateAPIView(TokenAPIViewForUpdate):
    model = Editor
    property_keyword = 'editors'
    serializer = EditorSerializerForUpdate

class EditorDeleteAPIView(TokenAPIViewForDeletion):
    model = Editor
```
上記において、`class EditorListAPIView(TokenAPIViewForList):` -> `dictionarizer = makeDictFromEditors` している。  
これは、継承元の common/views.py -> `class TokenAPIViewForList(TokenAPIView):` でレコードを辞書配列化する際にコールされる関数を指定している。`class TokenAPIViewForList(TokenAPIView):` 内では `self.dictionarizer(obj_editors)` のように `self.~` の形でコールする必要があり、その形でコールすると、必然的に第 1 引数にコールしたクラスが入り、第 2 引数に指定した `obj_editors` が渡ることになる。その為、コールされる editors/views.py -> `def makeDictFromEditors(model_editors):` 側は、第 1 引数にクラスが入り、第 2 引数に本来辞書配列化させたいオブジェクトを指定する形式に変更する。  

 - 変更前
```python
def makeDictFromEditors(model_editors):
```
 - 変更後
```python
def makeDictFromEditors(cls, model_editors):
```
また、すでにこの関数を同ファイル内でコールしている `def export_as_csv(request):` 内も以下の様に変更する
 - 変更前
```python
    dict_editors = makeDictFromEditors(obj_idSortedEditors) # 編集者リストを辞書配列化
```
 - 変更後
```python
    dict_editors = makeDictFromEditors(None, obj_idSortedEditors) # 編集者リストを辞書配列化
```

以上で、追加、読み込み、更新、削除時の処理定義は終わりだ。  
POST, GET, DELETE 時の共通処理を common/views.py に定義したので、今後新しい API を増やすときは、上記のような定義の追加だけで済む。  

## 動作確認

`python manage.py runserver` する。  

### 編集者の追加

追加する編集者情報を JSON 形式で以下のように作成する。
保存するディレクトリは任意の場所で構わない。 

#### Windows の場合

以降の例では、D:\jsontest 配下でファイルを作成したものとして説明を進める。

 - D:\jsontest\editors-to-create.json
```json
{
  "editors": [
    {
      "name": "sex unknown",
      "sex": ""
    },
    {
      "name": "male A",
      "sex": "男性"
    },
    {
      "name": "female A",
      "sex": "女性"
    }
  ]
}
```
そして、D:\jsontest をカレントディレクトリにしてコマンドプロンプトを開き、以下の様に実行する。  
(`authorization: Token eed5253~` に指定する文字列は、ユーザー一覧画面で行ったトークンの生成時に出力された文字列を指定する)  
```terminal
D:\jsontest>curl --header "authorization: Token eed52536051435f7ab5adfbea3831410d6694b65" "http://127.0.0.1:8000/api/v1/editors/create/" --verbose --data @editors-to-create.json
*   Trying 127.0.0.1:8000...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> POST /api/v1/editors/create/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.79.1
> Accept: */*
> authorization: Token eed52536051435f7ab5adfbea3831410d6694b65
> Content-Length: 184
> Content-Type: application/x-www-form-urlencoded
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Fri, 08 Apr 2022 11:03:13 GMT
< Server: WSGIServer/0.2 CPython/3.8.8rc1
< Content-Type: application/json
< Vary: Accept
< Allow: POST, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
{}* Connection #0 to host 127.0.0.1 left intact

D:\jsontest>
```
ブラウザで編集者の一覧画面に行けば、以下のように JSON ファイルで指定したデータがレコードとして登録されているはずだ。  

![](assets/images/2022-04-08-20-07-33.png)  

#### Mac の場合

以降の例では、~/jsontest 配下でファイルを作成したものとして説明を進める。

 - ~/jsontest/editors-to-create.json
```json
{
  "editors": [
    {
      "name": "sex unknown",
      "sex": ""
    },
    {
      "name": "male A",
      "sex": "男性"
    },
    {
      "name": "female A",
      "sex": "女性"
    }
  ]
}
```
そして、~/jsontest をカレントディレクトリにして terminal を開き、以下の様に実行する。  
(`authorization: Token eed5253~` に指定する文字列は、ユーザー一覧画面で行ったトークンの生成時に出力された文字列を指定する)  
```terminal
***@***noMBP jsontest % curl --header 'authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b' 'http://127.0.0.1:8000/api/v1/editors/create/' --verbose --data @editors-to-create.json
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> POST /api/v1/editors/create/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.64.1
> Accept: */*
> authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b
> Content-Length: 214
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 214 out of 214 bytes
< HTTP/1.1 200 OK
< Date: Sun, 10 Apr 2022 05:08:02 GMT
< Server: WSGIServer/0.2 CPython/3.8.8
< Content-Type: application/json
< Vary: Accept
< Allow: POST, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host 127.0.0.1 left intact
{}* Closing connection 0
***@***noMBP jsontest % 
```
ブラウザで編集者の一覧画面に行けば、以下のように JSON ファイルで指定したデータがレコードとして登録されているはずだ。  

![](assets/images/2022-04-10-14-12-08.png)  

### 編集者一覧の取得

#### Windows の場合

あらかじめ [jq-win64.exe](https://stedolan.github.io/jq/) を C:\Manually Installed\jq-win64\jq-win64.exe に配置したものとして説明する。    
コマンドプロンプトで以下のように実行する。  
```terminal
D:\jsontest>curl --header "authorization: Token eed52536051435f7ab5adfbea3831410d6694b65" "http://127.0.0.1:8000/api/v1/editors.json/" --verbose | "C:\Manually Installed\jq-win64\jq-win64.exe" > editors.json
*   Trying 127.0.0.1:8000...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /api/v1/editors.json/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.79.1
> Accept: */*
> authorization: Token eed52536051435f7ab5adfbea3831410d6694b65
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Fri, 08 Apr 2022 11:13:55 GMT
< Server: WSGIServer/0.2 CPython/3.8.8rc1
< Content-Type: application/json
< Vary: Accept
< Allow: GET, HEAD, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 134
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
{ [134 bytes data]
100   134  100   134    0     0   2513      0 --:--:-- --:--:-- --:--:--  2680
* Connection #0 to host 127.0.0.1 left intact

D:\jsontest>
```
すると、"D:\jsontest\editors.json" が作成され、以下のような内容になっているはずだ。

 - D:\jsontest\editors.json
```json
{
  "editors": [
    {
      "id": 1,
      "name": "sex unknown",
      "sex": ""
    },
    {
      "id": 2,
      "name": "male A",
      "sex": "男性"
    },
    {
      "id": 3,
      "name": "female A",
      "sex": "女性"
    }
  ]
}
```

#### Mac の場合

あらかじめ `brew install jq` して jq をインストールしたものとして説明する。  
terminal で以下のように実行する。  
```terminal
***@***noMBP jsontest % curl --header 'authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b' 'http://127.0.0.1:8000/api/v1/editors.json/' --verbose | jq > editors.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /api/v1/editors.json/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.64.1
> Accept: */*
> authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b
> 
< HTTP/1.1 200 OK
< Date: Sun, 10 Apr 2022 05:19:33 GMT
< Server: WSGIServer/0.2 CPython/3.8.8
< Content-Type: application/json
< Vary: Accept
< Allow: GET, HEAD, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 134
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
{ [134 bytes data]
100   134  100   134    0     0  11166      0 --:--:-- --:--:-- --:--:-- 11166
* Connection #0 to host 127.0.0.1 left intact
* Closing connection 0
***@***noMBP jsontest % 
```
すると、"~jsontest/editors.json" が作成され、以下のような内容になっているはずだ。

 - ~jsontest/editors.json
```json
{
  "editors": [
    {
      "id": 1,
      "name": "sex unknown",
      "sex": ""
    },
    {
      "id": 2,
      "name": "male A",
      "sex": "男性"
    },
    {
      "id": 3,
      "name": "female A",
      "sex": "女性"
    }
  ]
}
```

### 編集者の編集

#### Windows の場合

editors-to-update.json を作成し、内容を以下のようにする。  

 - editors-to-update.json
```json
{
  "editors": [
    {
      "id": 1,
      "name": "sex is male",
      "sex": "男性"
    },
    {
      "id": 2,
      "name": "female B",
      "sex": "女性"
    },
    {
      "id": 3,
      "name": "male B",
      "sex": "男性"
    }
  ]
}
```
そして、コマンドプロンプトで以下のように実行する。  
```terminal
D:\jsontest>curl --header "authorization: Token eed52536051435f7ab5adfbea3831410d6694b65" "http://127.0.0.1:8000/api/v1/editors/update/" --verbose --data @editors-to-update.json
*   Trying 127.0.0.1:8000...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> POST /api/v1/editors/update/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.79.1
> Accept: */*
> authorization: Token eed52536051435f7ab5adfbea3831410d6694b65
> Content-Length: 232
> Content-Type: application/x-www-form-urlencoded
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Fri, 08 Apr 2022 11:27:55 GMT
< Server: WSGIServer/0.2 CPython/3.8.8rc1
< Content-Type: application/json
< Vary: Accept
< Allow: POST, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
{}* Connection #0 to host 127.0.0.1 left intact

D:\jsontest>
```
ブラウザで編集者の一覧へ行けば、以下のように更新されているはずだ。  

![](assets/images/2022-04-08-20-32-01.png)  

#### Mac の場合

editors-to-update.json を作成し、内容を以下のようにする。  

 - editors-to-update.json
```json
{
  "editors": [
    {
      "id": 1,
      "name": "sex is male",
      "sex": "男性"
    },
    {
      "id": 2,
      "name": "female B",
      "sex": "女性"
    },
    {
      "id": 3,
      "name": "male B",
      "sex": "男性"
    }
  ]
}
```
そして、terminal で以下のように実行する。  
```terminal
***@***noMBP jsontest % curl --header 'authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b' 'http://127.0.0.1:8000/api/v1/editors/update/' --verbose --data @editors-to-update.json
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> POST /api/v1/editors/update/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.64.1
> Accept: */*
> authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b
> Content-Length: 268
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 268 out of 268 bytes
< HTTP/1.1 200 OK
< Date: Sun, 10 Apr 2022 05:26:51 GMT
< Server: WSGIServer/0.2 CPython/3.8.8
< Content-Type: application/json
< Vary: Accept
< Allow: POST, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host 127.0.0.1 left intact
{}* Closing connection 0
***@***noMBP jsontest % 
```
ブラウザで編集者の一覧へ行けば、以下のように更新されているはずだ。  

![](assets/images/2022-04-10-14-29-08.png)  

### 編集者の削除

#### Windows の場合

コマンドプロンプトで以下のように実行する。  
```terminal
D:\jsontest>curl --request DELETE --header "authorization: Token eed52536051435f7ab5adfbea3831410d6694b65" "http://127.0.0.1:8000/api/v1/editors/1/delete/" --verbose
*   Trying 127.0.0.1:8000...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> DELETE /api/v1/editors/1/delete/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.79.1
> Accept: */*
> authorization: Token eed52536051435f7ab5adfbea3831410d6694b65
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Fri, 08 Apr 2022 11:30:55 GMT
< Server: WSGIServer/0.2 CPython/3.8.8rc1
< Content-Type: application/json
< Vary: Accept
< Allow: DELETE, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
{}* Connection #0 to host 127.0.0.1 left intact

D:\jsontest>
```
ブラウザで編集者の一覧へ行けば、以下のように ID 1 のレコードが削除されているはずだ。  
![](assets/images/2022-04-08-20-32-38.png)  

#### Mac の場合

terminal で以下のように実行する。  
```terminal
***@***noMBP jsontest % curl --request DELETE --header 'authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b' 'http://127.0.0.1:8000/api/v1/editors/1/delete/' --verbose
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> DELETE /api/v1/editors/1/delete/ HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.64.1
> Accept: */*
> authorization: Token 0f8cc46a9d230cda2ae2af8a6477374f0fbedc6b
> 
< HTTP/1.1 200 OK
< Date: Sun, 10 Apr 2022 05:31:35 GMT
< Server: WSGIServer/0.2 CPython/3.8.8
< Content-Type: application/json
< Vary: Accept
< Allow: DELETE, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 2
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
< 
* Connection #0 to host 127.0.0.1 left intact
{}* Closing connection 0
***@***noMBP jsontest % 
```
ブラウザで編集者の一覧へ行けば、以下のように ID 1 のレコードが削除されているはずだ。  
![](assets/images/2022-04-10-14-32-53.png)  

#### [TIPS] curl のオプション

curl の実行時に使用している各オプションの意味は以下の通り。  

 - `--verbose` `-v`  
   https://curl.se/docs/manpage.html#-v  
   リクエストヘッダー、レスポンスヘッダーを標準出力に出力する  
   たとえば、以下のように出力される  
```
> GET /restapi/editors.json HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.79.1
> Accept: */*
> authorization: Token 6ec4afdb6ccaa5195e3dbc509147ed998060a2b9
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Wed, 06 Apr 2022 01:06:09 GMT
< Server: WSGIServer/0.2 CPython/3.8.8rc1
< Content-Type: application/json
< Vary: Accept
< Allow: GET, HEAD, OPTIONS
< X-Frame-Options: DENY
< Content-Length: 85
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
< Cross-Origin-Opener-Policy: same-origin
<
```
 - `--header` `-H`  
   https://curl.se/docs/manpage.html#-H  
   リクエストヘッダを指定する  
   例えば、以下のように指定する  
```
D:\>curl --header "authorization: Token 512ebc85cd4a1a1a5325a2d6203cecf65b5d94eb" "http://127.0.0.1:8000/restapi/editors.json"
```

 - `-d` `--data`  
   https://curl.se/docs/manpage.html#-d  
   データを指定する  
   例えば以下のように指定する  
   (`@` をつけると、ファイル名で指定できる)  
```
D:\>curl "http://127.0.0.1:8000/restapi/editors.json" --data "foo bar"
D:\>curl "http://127.0.0.1:8000/restapi/editors.json" --data @foobar.json
```

 - `-X` `--request`  
   https://curl.se/docs/manpage.html#-X  
   リクエストメソッドを指定する  
   例えば、以下のように指定する  
```
D:\>curl --request DELETE "http://127.0.0.1:8000/restapi/editors/1/delete"
```

## ここまでのソースコード

この項で実装したソースコードを、example/08-rest-api/main に置いた。 

# API Document

REST API を作成したので、その API に関するドキュメントを作成しよう。  
この PJ では、drf-spectacular という Python パッケージを利用して、ドキュメントを自動で生成させる仕組みを使って実装していく。  

## アプリケーションの登録

[公式ドキュメント](https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation) の記載どおりに、アプリケーションの登録と定義値の追加を行う。

 - main/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5', # テンプレートファイル内で `{% load django_bootstrap5 %}` するなら左記のように追記
    'widget_tweaks', # テンプレートファイル内で `{% load widget_tweaks %}` するなら左記のように追記
    'rest_framework', # Django REST framework の機能を使う場合は左記のように追記
    # 以下を追加
    'drf_spectacular', # Open API 準拠の API ドキュメント生成の為の定義 https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation
    'editors', # `~python.exe manage.py startapp xxx` で作成したアプリ名
    'accounts',
    'index',
]
~~~~~~~~~~~~~~~~~~~~~~~~~~Omitting~~~~~~~~~~~~~~~~~~~~~~~~~~
# 以下を追加

# Open API 準拠の API ドキュメント生成の為の定義
# https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # https://www.django-rest-framework.org/api-guide/parsers/#setting-the-parsers
    # note
    # 以下の設定で、
    # API ドキュメント (ReDoc 形式) の `REQUEST BODY SCHEMA` の欄が `application/json` に固定される
    # API ドキュメント (Swagger UI 形式) においては、`Request body` のプルダウンリストが `application/json` に固定される
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings

SPECTACULAR_SETTINGS = {
    'TITLE': 'Book Manager API',
    'DESCRIPTION': 'API documentation of Book Manager',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

## URL スキームの設計

URL スキームの設計も [公式ドキュメント](https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation) の通りだ。  

 - main/urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),

    # note
    # 第1引数には ``<`~python.exe manage.py startapp xxx` で作成したアプリ名>/`` を指定
    # 第2引数には ``include('<`~python.exe manage.py startapp xxx` で作成したアプリ名>.urls')`` を指定
    path('editors/', include('editors.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('index.urls')),
    # URL で API のメジャーバージョンが指定できるように、`v1/` を URL に追加
    path('api/v1/', include('common.apiv1_urls')),

    # 以下を追加
    
    # Open API 準拠の API ドキュメント生成の為の定義
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html#take-it-for-a-spin
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

## API ドキュメント用の OpenApiViewExtension クラスの作り込み

そして、API ドキュメントが生成される対象となるクラス OpenApiViewExtension を継承したクラスにドキュメントの内容を記載していく。
記載するべき内容は以下の実例を見たほうが早いだろう。  

editors/views.py の後半に以下の定義を追加する。

 - editors/views.py
```python

# ここ以降に Open API 準拠の API ドキュメント用定義を記載する
# note
# ここ以降の記載を例えば apidocs.py 等の別ファイルで定義しても API ドキュメントは生成されなかった。  
# (drf_spectacular の仕様で、view.py に記載された OpenApiViewExtension を継承したクラスについてドキュメントが生成されるものと思われる)  

from rest_framework import status, serializers

from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_serializer, OpenApiParameter, OpenApiResponse, OpenApiExample
# https://drf-spectacular.readthedocs.io/en/latest/drf_spectacular.html?highlight=openapiviewextension#drf_spectacular.extensions.OpenApiViewExtension
# https://drf-spectacular.readthedocs.io/en/latest/blueprints.html?highlight=Fixed#dj-stripe

from common.views import InvalidReasonSerializerForDoc

class EditorCreationSerializerForDoc(serializers.Serializer):
    name = serializers.CharField(help_text = '名前を指定します。他の編集者と同じの名前は登録できません。また、空文字も無効です。')
    sex = serializers.CharField(help_text = '任意で性別を指定します。', required = False)

class EditorCreationArraySerializerForDoc(serializers.Serializer):
    class EditorCreationSerializer(EditorCreationSerializerForDoc):
        pass
    editors = EditorCreationSerializer(many = True)

class EditorCreateOpenApiView(OpenApiViewExtension):

    target_class = EditorCreateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):
            
            # https://drf-spectacular.readthedocs.io/en/latest/readme.html?highlight=operation_id#customization-by-using-extend-schema
            @extend_schema(
                tags = ['編集者管理'],
                operation_id = '編集者の追加',
                description = '編集者を追加します。',
                request = EditorCreationArraySerializerForDoc,
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'JSON ファイルのパースエラーもしくはバリデーションエラー'
                    ),
                    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '`OperationalError` の発生。デッドロックの可能性。'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '性別指定 (男性)',
                        description = '性別指定 (男性)',
                        request_only = True,
                        value = {
                            "editors" : [
                                {
                                    "name" : "male A",
                                    "sex" : "男性"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別指定 (女性)',
                        description = '性別指定 (女性)',
                        request_only = True,
                        value = {
                            "editors" : [
                                {
                                    "name" : "female A",
                                    "sex" : "女性"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別未指定 (空文字)',
                        description = '性別未指定 (空文字)',
                        request_only = True,
                        value = {
                            "editors" : [
                                {
                                    "name" : "Foo Bar",
                                    "sex" : ""
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別未指定 (プロパティなし)',
                        description = '性別未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "editors" : [
                                {
                                    "name" : "Foo Bar"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = 'パースエラー (400 NG)',
                        description = 'JSON ファイルのパースエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 72 (char 71)\nrequest.body: b'{  \"editors\": [    {      \"name\": \"sex unknown\",      \"sex\": \"\"    }  ]'"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Editor が既に存在します。', code='invalid')]}"
                        },
                    ),
                    OpenApiExample(
                        name = 'OperationalError (500 NG)',
                        description = 'デッドロックの可能性 (500 NG)',
                        status_codes = [str(status.HTTP_500_INTERNAL_SERVER_ERROR)],
                        response_only = True,
                        value = {
                            "detail": "database is locked"
                        },
                    ),
                ],
            )

            def post(self, request, *args, **kwargs):
                pass

        return Fixed

class EditorListSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID')
    name = serializers.CharField(help_text = '名前')
    sex = serializers.CharField(help_text = '性別')

class EditorListupedArraySerializerForDoc(serializers.Serializer):
    class EditorListSerializer(EditorListSerializerForDoc):
        pass
    editors = EditorListSerializer(many = True)

class EditorListOpenApiView(OpenApiViewExtension):
    
    target_class = EditorListAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):
            
            @extend_schema(
                tags = ['編集者管理'],
                operation_id = '編集者一覧の取得',
                description = '編集者の一覧を取得します。',
                parameters = [
                    OpenApiParameter(name = 'id', description = 'ID', required = False, type = int),
                    OpenApiParameter(name = 'name', description = '名前', required = False, type = str),
                ],
                responses = {
                    status.HTTP_200_OK: OpenApiResponse(
                        response = EditorListupedArraySerializerForDoc,
                        description = '編集者の一覧'
                    ),
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'クエリ文字列 (クエリストリング) のパースエラー'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '200 OK',
                        description = '取得例 (200 OK)',
                        status_codes = [str(status.HTTP_200_OK)],
                        value = {
                            "editors": [
                                {
                                    "id": 1,
                                    "name": "sex unknown",
                                    "sex": ""
                                },
                                {
                                    "id": 2,
                                    "name": "male A",
                                    "sex": "男性"
                                },
                                {
                                    "id": 3,
                                    "name": "female A",
                                    "sex": "女性"
                                },
                            ]
                        },
                    ),
                    OpenApiExample(
                        name = '400 NG',
                        description = '取得例 (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        value = {
                            "detail": "Validation error found in /api/v1/editors.json?id=a"
                        },
                    ),
                ],
            )

            def get(self, request, *args, **kwargs):
                pass

        return Fixed

class EditorUpdateSerializerForDoc(serializers.Serializer):
    id = serializers.IntegerField(help_text = 'ID を指定します。存在しない ID は指定できません。')
    name = serializers.CharField(help_text = '名前を指定します。他の編集者と同じの名前は指定できません。また、空文字も無効です。')
    sex = serializers.CharField(help_text = '任意で性別を指定します。', required = False)

class EditorUpdatingArraySerializerForDoc(serializers.Serializer):
    class EditorUpdateSerializer(EditorUpdateSerializerForDoc):
        pass
    editors = EditorUpdateSerializer(many = True)

class EditorUpdateOpenApiView(OpenApiViewExtension):
    
    target_class = EditorUpdateAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):
            
            @extend_schema(
                tags = ['編集者管理'],
                operation_id = '編集者の編集',
                description = '編集者の情報を更新します。',
                request = EditorUpdatingArraySerializerForDoc,
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = 'JSON ファイルのパースエラーもしくはバリデーションエラー'
                    ),
                    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '`OperationalError` の発生。デッドロックの可能性。'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '性別指定 (男性)',
                        description = '性別指定 (男性)',
                        request_only = True,
                        value = {
                            "editors": [
                                {
                                    "id" : 1,
                                    "name" : "male A",
                                    "sex" : "男性"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別指定 (女性)',
                        description = '性別指定 (女性)',
                        request_only = True,
                        value = {
                            "editors": [
                                {
                                    "id" : 1,
                                    "name" : "female A",
                                    "sex" : "女性"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別未指定 (空文字)',
                        description = '性別未指定 (空文字)',
                        request_only = True,
                        value = {
                            "editors": [
                                {
                                    "id" : 1,
                                    "name" : "Foo Bar",
                                    "sex" : ""
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = '性別未指定 (プロパティなし)',
                        description = '性別未指定 (プロパティなし)',
                        request_only = True,
                        value = {
                            "editors": [
                                {
                                    "id" : 1,
                                    "name" : "Foo Bar"
                                }
                            ]
                        }
                    ),
                    OpenApiExample(
                        name = 'パースエラー (400 NG)',
                        description = 'JSON ファイルのパースエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "JSONDecodeError occured while `json.loads`. Check following.\nError message: Expecting ',' delimiter: line 1 column 72 (char 71)\nrequest.body: b'{  \"editors\": [    {      \"name\": \"sex unknown\",      \"sex\": \"\"    }  ]'"
                        },
                    ),
                    OpenApiExample(
                        name = 'バリデーションエラー (400 NG)',
                        description = '登録する情報のバリデーションエラー (400 NG)',
                        status_codes = [str(status.HTTP_400_BAD_REQUEST)],
                        response_only = True,
                        value = {
                            "detail": "Validation error: {'non_field_errors': [ErrorDetail(string='この 名前 を持った Editor が既に存在します。', code='invalid')]}"
                        },
                    ),
                    OpenApiExample(
                        name = 'OperationalError (500 NG)',
                        description = 'デッドロックの可能性 (500 NG)',
                        status_codes = [str(status.HTTP_500_INTERNAL_SERVER_ERROR)],
                        response_only = True,
                        value = {
                            "detail": "database is locked"
                        },
                    ),
                ]
            )

            def post(self, request, *args, **kwargs):
                pass

        return Fixed


class EditorDeleteOpenApiView(OpenApiViewExtension):
    
    target_class = EditorDeleteAPIView

    def view_replacement(self):
        
        class Fixed(self.target_class):

            @extend_schema(
                tags = ['編集者管理'],
                operation_id = '編集者の削除',
                description = '指定 ID の編集者を削除します。',
                parameters = [
                    OpenApiParameter(name = 'id', description = 'ID', location = OpenApiParameter.PATH , type = int),
                ],
                responses = {
                    status.HTTP_200_OK: None,
                    status.HTTP_404_NOT_FOUND: OpenApiResponse(
                        response = InvalidReasonSerializerForDoc,
                        description = '指定 ID が存在しないエラー'
                    ),
                },
                examples = [
                    OpenApiExample(
                        name = '指定 ID 検索エラー (404 NG)',
                        description = '指定 ID が存在しないエラー (400 NG)',
                        status_codes = [str(status.HTTP_404_NOT_FOUND)],
                        value = {
                            "detail": "Specified Editor ID: 1 not found."
                        },
                    ),
                ]
            )

            def delete(self, request, pk, *args, **kwargs):
                pass

        return Fixed
```

そして、common/views.py に以下の定義を追加する。  

 - common/views.py
```python
# ここ以降に Open API 準拠の API ドキュメント用定義を記載する

from rest_framework import serializers

class InvalidReasonSerializerForDoc(serializers.Serializer):
    detail = serializers.CharField(help_text = 'エラーメッセージ')
```

## html ファイルの作り込み

あとはナビバーに API ドキュメントへのリンクを作成したいので、templates/base.html の内容を以下のように変更する
 - 変更前
```html
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuAccounts">
            <li>
              <a class="dropdown-item" href="{% url 'accounts:list' %}">ユーザーの一覧</a>
            </li>
            {% if user.is_authenticated %}
            <li>
              <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#logoutModal">ログアウト</button>
            </li>
            {% endif %}
          </ul>
```
 - 変更後
```html
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuAccounts">
            <li>
              <a class="dropdown-item" href="{% url 'accounts:list' %}">ユーザーの一覧</a>
            </li>
            <li>
              <a class="dropdown-item" href="{% url 'swagger-ui' %}">API ドキュメント (Swagger UI)</a>
            </li>
            <li>
              <a class="dropdown-item" href="{% url 'redoc' %}">API ドキュメント (ReDoc)</a>
            </li>
            {% if user.is_authenticated %}
            <li>
              <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#logoutModal">ログアウト</button>
            </li>
            {% endif %}
          </ul>
```

## 動作確認

### Swagger UI

ナビバーの右上ドロップダウンメニューから `API ドキュメント (Swagger UI)` を選択する。

![](assets/images/2022-04-14-15-06-48.png)  

すると、Swagger UI 形式と呼ばれる形式の APi ドキュメントが参照できる。  
`Authorize` で以下のように認証トークンを指定すれば、

![](assets/images/swagger-ui-01.svg)  

以下のように API の実行をこの UI から行うことができる。  

![](assets/images/swagger-ui-02.svg)  

### ReDoc

ナビバーの右上ドロップダウンメニューから `API ドキュメント (Swagger UI)` を選択する。  

![](assets/images/2022-04-14-15-25-00.png)  

すると、ReDoc 形式と呼ばれる形式の APi ドキュメントが参照できる。  

![](assets/images/2022-04-14-15-26-04.png)  

## ここまでのソースコード

この項で実装したソースコードを、example/09-api-document/main に置いた。 

# 単体テスト

```
python manage.py test -v2 accounts
coverage run --source=. manage.py test accounts common editors
coverage html
```
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django Unit Test",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}\\manage.py", //<- Windows の場合。 Mac の場合は `"${workspaceFolder}/manage.py"` とする
            "args": [
                "test",
                "-v2",
                "accounts",
                "common",
                "editors",
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}
```