import datetime
import json
import re
import textwrap

from unittest import mock

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.test import TestCase
from django.test import TransactionTestCase
from django.utils.timezone import make_aware

from accounts.models import TokenForRESTAPI

from common.const import INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK, STR_ATTRIBUTE_KEYWORD_FOR_TOKEN

from authors.models import Author
from authors.views import makeDictFromAuthors

# Create your tests here.

class AuthorCreateTest(TestCase):
    """ AuthorCreate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

    def test_001(self):
        """
        使用するテンプレートファイルが正しいかどうか確認する
        """
        obj_response =  self.client.get('/authors/create/')
        self.assertTemplateUsed(obj_response, 'authors/form.html')

    def test_002(self):
        """
        著者登録に成功した際に著者一覧画面にリダイレクトされることを確認する
        """
        dict_toSaveAuthor = {
            'name': 'toSaveAuthor',
            'birthday': '2000-06-10'
        }
        obj_response = self.client.post('/authors/create/', data = dict_toSaveAuthor)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_savedAuthor = Author.objects.filter(name = dict_toSaveAuthor['name']).first()
        self.assertTrue(obj_savedAuthor)
        self.assertEqual(obj_savedAuthor.birthday, datetime.date(2000, 6, 10))

class AuthorsListTest(TestCase):
    """ AuthorsList """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

    def test_001(self):
        """
        著者一覧に使用されるテンプレートが正しいかどうか確認する
        """
        obj_toCreateAuthor = Author.objects.create(
            name = 'toCreateAuthor'
        )
        obj_response =  self.client.get('/authors/')
        self.assertTemplateUsed(obj_response, 'authors/list.html')
        self.assertContains(obj_response, obj_toCreateAuthor.name, status_code = 200)

class AuthorUpdateTest(TestCase):
    """ AuthorUpdate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createdAuthor, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdAuthor',
                'birthday': None,
            }
        )

    def test_001(self):
        """
        著者の編集画面に使用されるテンプレートが正しいかどうか確認する
        """
        obj_response =  self.client.get(f'/authors/{self.obj_createdAuthor.id}/update/')
        self.assertTemplateUsed(obj_response, 'authors/form.html')

    def test_002(self):
        """
        著者の編集成功時に正しい URL へリダイレクトされるかどうか確認する
        """
        dict_toUpdateAuthor = {
            'name': 'updatedAuthor',
        }
        obj_response =  self.client.post(f'/authors/{self.obj_createdAuthor.id}/update/', data = dict_toUpdateAuthor)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')
        self.assertTrue(Author.objects.filter(name = dict_toUpdateAuthor['name']).first())

class AuthorDeleteTest(TestCase):
    """ AuthorDelete """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createdAuthor, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdAuthor',
                'birthday': datetime.date(2000, 10 ,10),
            }
        )

    def test_001(self):
        """
        著者の削除成功時に正しい URL へリダイレクトされるかどうか確認する
        """

        obj_response =  self.client.delete(f'/authors/{self.obj_createdAuthor.id}/delete/')
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')
        self.assertFalse(Author.objects.filter(name = self.obj_createdAuthor.name).first())

class makeDictFromAuthorsTest(TransactionTestCase):
    """ makeDictFromAuthors """

    reset_sequences = True

    def setUp(self):
        self.dict_authors = []
        self.dict_authors.append(
            Author.objects.create(
                name = 'author A',
            )
        )
        self.dict_authors.append(
            Author.objects.create(
                name = 'author B',
                birthday = None,
            )
        )
        self.dict_authors.append(
            Author.objects.create(
                name = 'sex unknown',
                birthday = datetime.date(2000, 10 ,10),
            )
        )

    def test_001(self):
        """
        著者リストを辞書配列化する
        """
        dict_expectedAuthors = [
            {
                'id': 1,
                'name': 'author A',
                'birthday': None
            },
            {
                'id': 2,
                'name': 'author B',
                'birthday': None
            },
            {
                'id': 3,
                'name': 'sex unknown',
                'birthday': datetime.date(2000, 10 ,10)
            },
        ]
        self.assertEqual(makeDictFromAuthors(None, self.dict_authors), dict_expectedAuthors)

class export_as_csvTest(TransactionTestCase):
    """ export_as_csv """

    reset_sequences = True

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        
        Author.objects.create(
            name = 'author A',
        )
        Author.objects.create(
            name = 'author B',
            birthday = None,
        )
        Author.objects.create(
            name = 'sex unknown',
            birthday = datetime.date(2000, 10 ,13),
        )

    def test_001(self):
        """
        CSV 形式で出力されることを確認
        """
        obj_response = self.client.get('/authors/export_as_csv/')
        self.assertEqual(obj_response.status_code, 200)

        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

class import_from_csvTest(TransactionTestCase):
    """ import_from_csv """

    reset_sequences = True

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        
        Author.objects.create(
            name = 'author A',
        )
        Author.objects.create(
            name = 'author B',
            birthday = None,
        )
        Author.objects.create(
            name = 'sex unknown',
            birthday = datetime.date(2000, 10 ,13),
        )
    
    def test_001(self):
        """
        CSVImputForm のバリデーションエラー
        """

        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,"added, name",
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_002(self):
        """
        UnicodeDecodeError
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,"added, name",
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText.encode('shift-jis'))
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_003(self):
        """
        必要なカラムタイトルが存在しない
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前
            4,"added, name"
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_004(self):
        """
        バリデーションエラーとなるレコードが一部存在する
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,added name,2000-12-30
            5.added name2,2000/12/30
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
            4,added name,2000-12-30
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_005(self):
        """
        名前フィールドが他レコードと重複している
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,sex unknown,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_006(self):
        """
        置き換えモードで全て削除
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'replace',
        }

        obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_007(self):
        """
        デッドロックの発生(既定回数内)
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,added name,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'authors.views.Author.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * (INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK - 1) +
                [Author.objects.update_or_create(
                    id = 4,
                    defaults = {
                        'name': 'added name',
                        'birthday': None
                    }
                )],
        ):
            obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
            4,added name,
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

    def test_008(self):
        """
        デッドロックの発生(既定回数超過)
        """
        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,生年月日
            4,added name,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'authors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'authors.views.Author.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK,
        ):
            obj_response = self.client.post('/authors/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/authors/')

        obj_response = self.client.get('/authors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,生年月日
            1,author A,
            2,author B,
            3,sex unknown,2000-10-13
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

class AuthorCreateAPIViewTest(TestCase):
    """ AuthorCreateAPIView """

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        名前の重複
        """
        Author.objects.create(
            name = 'male A',
            birthday = datetime.date(1999, 12, 24),
        )
        str_input = textwrap.dedent('''\
            {
                "authors": [
                    {
                        "name": "male A",
                        "birthday": "1999-12-25"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/authors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Author が既に存在します。', status_code = 400)

    def test_002(self):
        """
        `birthday` プロパティの未指定
        """
        str_input = textwrap.dedent('''\
            {
                "authors": [
                    {
                        "name": "male A"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/authors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Author.objects.filter(name = 'male A').first().birthday, None)

class AuthorListAPIViewTest(TestCase):
    """ AuthorListAPIView """

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        クエリ文字列のバリデーション OK
        """
        null = None

        Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'maleA',
                'birthday': datetime.date(1984, 11, 30),
            }
        )
        self.obj_id2, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name':'femaleA',
                'birthday': None,
            }
        )

        dict_expected = {
            'authors': [
                {
                    'id': 2,
                    'name': 'femaleA',
                    'birthday': null,
                },
            ]
        }

        obj_response = self.client.get(f'/api/v1/authors.json/?id={self.obj_id2.id}&name={self.obj_id2.name}', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), dict_expected)

class AuthorUpdateAPIViewTest(TestCase):
    """ AuthorUpdateAPIView """

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
        )


    def test_001(self):
        """
        名前フィールドの重複
        """

        Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'maleA',
                'birthday': datetime.date(1984, 11, 30),
            }
        )
        self.obj_id2, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name':'femaleA',
                'birthday': None,
            }
        )
        str_input = textwrap.dedent(f'''\
            {{
                "authors": [
                    {{
                        "id": {self.obj_id2.id},
                        "name": "maleA"
                    }}
                ]
            }}
        ''')
        obj_response = self.client.post(
            '/api/v1/authors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Author が既に存在します。', status_code = 400)

    def test_002(self):
        """
        バリデーションOK
        """

        self.obj_id1, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'femaleA',
                'birthday': datetime.date(1984, 11, 30),
            }
        )
        str_input = textwrap.dedent(f'''\
            {{
                "authors": [
                    {{
                        "id": {self.obj_id1.id},
                        "name": "updated name"
                    }}
                ]
            }}
        ''')
        obj_response = self.client.post(
            '/api/v1/authors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )

        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Author.objects.filter(name = 'updated name').first().birthday, None)

class AuthorDeleteAPIViewTest(TestCase):
    """ AuthorDeleteAPIView """

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        削除成功
        """

        obj_toDeleteAuthor, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'maleA',
                'birthday': None,
            }
        )

        obj_response = self.client.delete(
            f'/api/v1/authors/{obj_toDeleteAuthor.id}/delete/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}'
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Author.objects.filter(id = obj_toDeleteAuthor.id).first(), None)
