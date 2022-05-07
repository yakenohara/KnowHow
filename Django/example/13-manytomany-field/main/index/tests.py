import datetime
import json
import re
import textwrap

from unittest import mock

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.test import TestCase
from django.utils.timezone import make_aware

from accounts.models import TokenForRESTAPI

from authors.models import Author

from editors.models import Editor

from common.const import INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK, STR_ATTRIBUTE_KEYWORD_FOR_TOKEN

from index.views import makeDictFromBooks, makeDictFromBooksForRESTAPI
from index.models import Book

# Create your tests here.

class BookCreateTest(TestCase):
    """ BookCreate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdAuthor',
                'birthday': None,
            }
        )
        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdEditor1',
                'sex': Editor.Sex.FEMALE,
            }
        )
        Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'createdEditor2',
                'sex': None,
            }
        )

    def test_001(self):
        """
        使用するテンプレートファイルが正しいかどうか確認する
        """
        obj_response =  self.client.get('/create/')
        self.assertTemplateUsed(obj_response, 'index/form.html')

    def test_002(self):
        """
        書籍登録に成功した際に著者一覧画面にリダイレクトされることを確認する(外部キー参照なし)
        """
        dict_toSaveBook = {
            'name': 'toSaveBook',
            'author': '',
            'editors': [],
        }
        obj_response = self.client.post('/create/', data = dict_toSaveBook)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_savedBook = Book.objects.filter(name = dict_toSaveBook['name']).first()
        self.assertTrue(obj_savedBook)
        self.assertEqual(obj_savedBook.author, None)

    def test_003(self):
        """
        書籍登録に成功した際に著者一覧画面にリダイレクトされることを確認する(外部キー参照あり)
        """
        dict_toSaveBook = {
            'name': 'toSaveBook',
            'author': 1,
            'editors': [1, 2]
        }
        obj_response = self.client.post('/create/', data = dict_toSaveBook)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_savedBook = Book.objects.filter(name = dict_toSaveBook['name']).first()
        self.assertTrue(obj_savedBook)
        self.assertEqual(obj_savedBook.author.name, 'createdAuthor')

class IndexTest(TestCase):
    """ Index """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

    def test_001(self):
        """
        書籍一覧に使用されるテンプレートが正しいかどうか確認する
        """
        obj_toCreateBook = Book.objects.create(
            name = 'created book'
        )
        obj_response =  self.client.get('/')
        self.assertTemplateUsed(obj_response, 'index/index.html')
        self.assertContains(obj_response, obj_toCreateBook.name, status_code = 200)

class BookUpdateTest(TestCase):
    """ BookUpdate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createBook, _ = Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created book',
                'author': None,
            }
        )
        Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created author',
                'birthday': datetime.date(2000, 6, 10),
            }
        )
        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdEditor1',
                'sex': None,
            }
        )
        Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'createdEditor2',
                'sex': None,
            }
        )

    def test_001(self):
        """
        書籍の編集画面に使用されるテンプレートが正しいかどうか確認する
        """
        obj_response =  self.client.get(f'/{self.obj_createBook.id}/update/')
        self.assertTemplateUsed(obj_response, 'index/form.html')

    def test_002(self):
        """
        著者の編集成功時に正しい URL へリダイレクトされるかどうか確認する(外部キー参照なし)
        """
        dict_toUpdateBook = {
            'name': 'updated book',
            'author': '',
            'editors': [],
        }
        obj_response =  self.client.post(f'/{self.obj_createBook.id}/update/', data = dict_toUpdateBook)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')
        self.assertTrue(Book.objects.filter(name = dict_toUpdateBook['name']).first())
    
    def test_003(self):
        """
        著者の編集成功時に正しい URL へリダイレクトされるかどうか確認する(外部キー参照あり)
        """
        dict_toUpdateBook = {
            'name': 'updated book',
            'author': 1,
            'editors': [1,2],
        }
        obj_response =  self.client.post(f'/{self.obj_createBook.id}/update/', data = dict_toUpdateBook)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')
        self.assertEqual(Book.objects.filter(name = dict_toUpdateBook['name']).first().author.birthday, datetime.date(2000, 6, 10))

class BookDeleteTest(TestCase):
    """ BookDelete """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createdBook, _ = Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created book',
                'author': None,
            }
        )

    def test_001(self):
        """
        著者の削除成功時に正しい URL へリダイレクトされるかどうか確認する
        """

        obj_response =  self.client.delete(f'/{self.obj_createdBook.id}/delete/')
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')
        self.assertFalse(Author.objects.filter(name = self.obj_createdBook.name).first())

class makeDictFromBooksTest(TestCase):
    """ makeDictFromBooks """

    def setUp(self):

        obj_createdAuthorA, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created author A',
                'birthday': datetime.date(1999, 12, 13),
            }
        )

        obj_createdAuthorB, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created author B',
                'birthday': datetime.date(1999, 12, 13),
            }
        )

        obj_createdEditorA, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created editor A',
                'sex': Editor.Sex.FEMALE,
            }
        )

        obj_createdEditorB, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created editor B',
                'sex': None,
            }
        )

        self.dict_books = []
        self.dict_books.append(
            Book.objects.create(
                name = 'book A',
                author = obj_createdAuthorA
            )
        )
        self.dict_books.append(
            Book.objects.create(
                name = 'book B',
                author = obj_createdAuthorB,
            )
        )
        self.dict_books.append(
            Book.objects.create(
                name = 'book C',
                author = None,
            )
        )
        self.dict_books[2].editors.set([obj_createdEditorA, obj_createdEditorB])
        self.dict_books[2].save()

    def test_001(self):
        """
        著者リストを辞書配列化する
        """
        dict_expectedBooks = [
            {
                'id': 1,
                'name': 'book A',
                'author': 'created author A',
                'editors': '',
            },
            {
                'id': 2,
                'name': 'book B',
                'author': 'created author B',
                'editors': '',
            },
            {
                'id': 3,
                'name': 'book C',
                'author': '',
                'editors': 'created editor A,created editor B',
            },
        ]
        self.assertEqual(makeDictFromBooks(None, self.dict_books), dict_expectedBooks)

class makeDictFromBooksForRESTAPITest(TestCase):
    """ makeDictFromBooksForRESTAPI """

    def setUp(self):

        obj_createdAuthorA, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created author A',
                'birthday': datetime.date(1999, 12, 13),
            }
        )

        obj_createdAuthorB, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created author B',
                'birthday': datetime.date(1999, 12, 13),
            }
        )

        obj_createdEditorA, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created editor A',
                'sex': Editor.Sex.FEMALE,
            }
        )

        obj_createdEditorB, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created editor B',
                'sex': None,
            }
        )

        self.dict_books = []
        self.dict_books.append(
            Book.objects.create(
                name = 'book A',
                author = obj_createdAuthorA
            )
        )
        self.dict_books.append(
            Book.objects.create(
                name = 'book B',
                author = obj_createdAuthorB,
            )
        )
        self.dict_books.append(
            Book.objects.create(
                name = 'book C',
                author = None,
            )
        )
        self.dict_books[2].editors.set([obj_createdEditorA, obj_createdEditorB])
        self.dict_books[2].save()

    def test_001(self):
        """
        著者リストを辞書配列化する
        """
        dict_expectedBooks = [
            {
                'id': 1,
                'name': 'book A',
                'author': 'created author A',
                'editors': [],
            },
            {
                'id': 2,
                'name': 'book B',
                'author': 'created author B',
                'editors': [],
            },
            {
                'id': 3,
                'name': 'book C',
                'author': '',
                'editors': [
                    'created editor A',
                    'created editor B'
                ]
            },
        ]
        self.assertEqual(makeDictFromBooksForRESTAPI(None, self.dict_books), dict_expectedBooks)

class export_as_csvTest(TestCase):
    """ export_as_csv """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        
        obj_authorA, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'author A',
            }
        )
        obj_authorB, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'author B',
                'birthday': None,
            }
        )
        obj_authorC, _ = Author.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'author C',
                'birthday': datetime.date(2000, 10 ,13),
            }
        )

        obj_createdEditorA, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created editor A',
                'sex': Editor.Sex.FEMALE,
            }
        )

        obj_createdEditorB, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created editor B',
                'sex': None,
            }
        )

        Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'book A',
                'author': obj_authorA
            }
        )
        Book.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'book B',
                'author': obj_authorB
            }
        )
        Book.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'book C',
                'author': obj_authorC
            }
        )
        obj_book, _ = Book.objects.update_or_create(
            id = 4,
            defaults = {
                'name': 'book D',
                'author': None
            }
        )
        obj_book.editors.set([obj_createdEditorA, obj_createdEditorB])
        obj_book.save()
        
    def test_001(self):
        """
        CSV 形式で出力されることを確認
        """
        obj_response = self.client.get('/export_as_csv/')
        self.assertEqual(obj_response.status_code, 200)

        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

class import_from_csvTest(TestCase):
    """ import_from_csv """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        
        obj_authorA, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'author A',
            }
        )
        obj_authorB, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'author B',
                'birthday': None,
            }
        )
        obj_authorC, _ = Author.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'author C',
                'birthday': datetime.date(2000, 10 ,13),
            }
        )

        obj_createdEditorA, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created editor A',
                'sex': Editor.Sex.FEMALE,
            }
        )

        obj_createdEditorB, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created editor B',
                'sex': None,
            }
        )

        Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'book A',
                'author': obj_authorA
            }
        )
        Book.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'book B',
                'author': obj_authorB
            }
        )
        Book.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'book C',
                'author': obj_authorC
            }
        )
        obj_book, _ = Book.objects.update_or_create(
            id = 4,
            defaults = {
                'name': 'book D',
                'author': None
            }
        )
        obj_book.editors.set([obj_createdEditorA, obj_createdEditorB])
        obj_book.save()

    def test_001(self):
        """
        CSVImputForm のバリデーションエラー
        """

        str_toImportCSVText = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            5,"added, name",,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
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
            ID,著書名,著者名,編集者名
            5,"added, name",,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText.encode('shift-jis'))
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
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
            ID,著書名,著者名
            5,"added, name",
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
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
            ID,著書名,著者名,編集者名
            5,"added, name",author C,"created editor A,created editor B"
            6,added name,author D,
            7,added name,,\\
            8,added name,,\\a
            9,added name,,created editor C
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
            5,"added, name",author C,"created editor A,created editor B"
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
            ID,著書名,著者名,編集者名
            5,book D,,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
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
            ID,著書名,著者名,編集者名
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'replace',
        }

        obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
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
            ID,著書名,著者名,編集者名
            5,added name,,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'index.views.Book.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * (INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK - 1) +
                [Book.objects.update_or_create(
                    id = 5,
                    defaults = {
                        'name': 'added name',
                        'author': None
                    }
                )],
        ):
            obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
            5,added name,,
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
            ID,著書名,著者名,編集者名
            5,added name,,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'books.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'index.views.Book.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK,
        ):
            obj_response = self.client.post('/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

        obj_response = self.client.get('/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,著書名,著者名,編集者名
            1,book A,author A,
            2,book B,author B,
            3,book C,author C,
            4,book D,,"created editor A,created editor B"
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

class BookCreateAPIViewTest(TestCase):
    """ BookCreateAPIView """

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

        Book.objects.create(
            name = 'created book',
            author = None,
        )
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "author": ""
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Book が既に存在します。', status_code = 400)

    def test_002(self):
        """
        存在しない著者名
        """

        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "author": "Author A"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, '指定された著者名 `Author A` は存在しません。', status_code = 400)

    def test_003(self):
        """
        author フィールドの指定
        """
        Author.objects.create(
            name = 'Author A',
            birthday = datetime.date(1999, 12, 24),
        )
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "author": "Author A"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'created book').author.birthday, datetime.date(1999, 12, 24))

    def test_004(self):
        """
        author フィールドの未指定
        """

        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'created book').author, None)

    def test_005(self):
        """
        author フィールドの空文字指定
        """

        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "author": ""
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'created book').author, None)

    def test_006(self):
        """
        存在しない編集者名
        """

        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "editors": [
                            "editor A"
                        ]
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, '指定された編集者名 `editor A` は存在しません。', status_code = 400)


    def test_007(self):
        """
        editors フィールドの指定
        """

        Editor.objects.create(
            name = 'Editor A',
            sex = Editor.Sex.FEMALE,
        )
        Editor.objects.create(
            name = 'Editor B',
            sex = None,
        )
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "editors": [
                            "Editor A",
                            "Editor B"
                        ]
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'created book').editors.all()[0].name, 'Editor A')
        self.assertEqual(Book.objects.get(name = 'created book').editors.all()[1].name, 'Editor B')

    def test_008(self):
        """
        editors フィールドの空指定
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "name": "created book",
                        "editors": []
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'created book').editors.all().count(), 0)

class BookListAPIViewTest(TestCase):
    """ BookListAPIView """

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

        obj_authorA, _ = Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'author A',
            }
        )
        obj_authorB, _ = Author.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'author B',
                'birthday': None,
            }
        )
        obj_authorC, _ = Author.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'author C',
                'birthday': datetime.date(2000, 10 ,13),
            }
        )

        Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'book A',
                'author': obj_authorA
            }
        )
        Book.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'book B',
                'author': obj_authorB
            }
        )
        editor1, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdEditor1',
                'sex': Editor.Sex.FEMALE,
            }
        )
        editor2, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'createdEditor2',
                'sex': None,
            }
        )
        obj_id3, _ = Book.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'book C',
                'author': obj_authorC
            }
        )
        obj_id3.editors.set([editor1, editor2])
        obj_id3.save()
        Book.objects.update_or_create(
            id = 4,
            defaults = {
                'name': 'book D',
                'author': None
            }
        )

        dict_expected = {
            'books': [
                {
                    'id': 3,
                    'name': 'book C',
                    'author': 'author C',
                    'editors': [
                        "createdEditor1",
                        "createdEditor2"
                    ]
                },
            ]
        }

        obj_response = self.client.get(f'/api/v1/books.json/?id={obj_id3.id}&name={obj_id3.name}', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), dict_expected)

class BookUpdateAPIViewTest(TestCase):
    """ BookUpdateAPIView """

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

        Author.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'author A',
            }
        )
        
        Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created book 1',
                'author': None,
            }
        )
        Book.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created book 2',
                'author': None,
            }
        )

    def test_001(self):
        """
        名前の重複
        """

        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "created book 1",
                        "author": ""
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Book が既に存在します。', status_code = 400)

    def test_002(self):
        """
        著者指定
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "author": "author A"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'updated book').author.name, 'author A')

    def test_003(self):
        """
        存在しない著者名
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "author": "author B"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, '指定された著者名 `author B` は存在しません。', status_code = 400)

    def test_004(self):
        """
        著者名の未指定
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'updated book').author, None)

    def test_005(self):
        """
        著者名の空文字指定
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "author": ""
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'updated book').author, None)

    def test_006(self):
        """
        存在しない編集者名
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "editors": [
                            "Editor A"
                        ]
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 400)
        self.assertEqual(Book.objects.get(name = 'created book 1').editors.all().first(), None)

    def test_007(self):
        """
        editors フィールドの指定
        """

        Editor.objects.create(
            name = 'Editor A',
            sex = Editor.Sex.FEMALE,
        )
        Editor.objects.create(
            name = 'Editor B',
            sex = None,
        )
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "editors": [
                            "Editor A",
                            "Editor B"
                        ]
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'updated book').editors.all()[0].name, 'Editor A')
        self.assertEqual(Book.objects.get(name = 'updated book').editors.all()[1].name, 'Editor B')

    def test_008(self):
        """
        editors フィールドの空指定
        """
        str_input = textwrap.dedent('''\
            {
                "books": [
                    {
                        "id": 2,
                        "name": "updated book",
                        "editors": []
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/books/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.get(name = 'updated book').editors.all().count(), 0)


class BookDeleteAPIViewTest(TestCase):
    """ BookDeleteAPIView """

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

        self.obj_book1, _ = Book.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'created book 1',
                'author': None,
            }
        )
        self.obj_book2, _ = Book.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'created book 2',
                'author': None,
            }
        )
    
    def test_001(self):
        """
        削除成功
        """
        obj_response = self.client.delete(
            f'/api/v1/books/{self.obj_book1.id}/delete/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}'
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Book.objects.filter(id = self.obj_book1.id).first(), None)

    def test_002(self):
        """
        削除失敗
        """
        obj_response = self.client.delete(
            f'/api/v1/books/3/delete/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}'
        )
        self.assertContains(obj_response, 'Specified Book ID: 3 not found.', status_code = 404)
