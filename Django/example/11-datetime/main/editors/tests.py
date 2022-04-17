import datetime
import json
import re
import textwrap

from unittest import mock

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.test import TestCase

from accounts.models import TokenForRESTAPI

from common.const import INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK, STR_ATTRIBUTE_KEYWORD_FOR_TOKEN

from editors.models import Editor
from editors.serializer import EditorSerializerForQueryString
from editors.views import makeDictFromEditors

# Create your tests here.

class EditorCreateTest(TestCase):
    """ EditorCreate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
    
    def test_001(self):
        """
        編集者登録画面で使うテンプレートファイルが正しいかどうか確認する
        """
        obj_response =  self.client.get('/editors/create/')
        self.assertTemplateUsed(obj_response, 'editors/form.html')

    def test_002(self):
        """
        編集者登録に成功した際に編集者一覧画面にリダイレクトされることを確認する
        """

        dict_toSaveEditor = {
            'name': 'toSaveEditor',
            'sex': Editor.Sex.FEMALE.value
        }
        obj_response = self.client.post('/editors/create/', data = dict_toSaveEditor)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_savedEditor = Editor.objects.filter(name = dict_toSaveEditor['name']).first()
        self.assertTrue(obj_savedEditor)
        self.assertEqual(obj_savedEditor.sex, dict_toSaveEditor['sex'])

class EditorsListTest(TestCase):
    """ EditorsList """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

    def test_001(self):
        """
        編集者一覧に使用されるテンプレートが正しいかどうか確認する
        """
        obj_toCreateEditor = Editor.objects.create(
            name = 'toCreateEditor',
            sex = Editor.Sex.MALE
        )
        obj_response =  self.client.get('/editors/')
        self.assertTemplateUsed(obj_response, 'editors/list.html')
        self.assertContains(obj_response, obj_toCreateEditor.name, status_code = 200)

class EditorUpdateTest(TestCase):
    """ EditorUpdate """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createdEditor, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdEditor',
                'sex': Editor.Sex.FEMALE,
            }
        )

    def test_001(self):
        """
        編集者の編集画面に使用されるテンプレートが正しいかどうか確認する
        """
        obj_response =  self.client.get(f'/editors/{self.obj_createdEditor.id}/update/')
        self.assertTemplateUsed(obj_response, 'editors/form.html')
    
    def test_002(self):
        """
        編集者の編集成功時に正しい URL へリダイレクトされるかどうか確認する
        """
        dict_toUpdateEditor = {
            'name': 'updatedEditor',
        }
        obj_response =  self.client.post(f'/editors/{self.obj_createdEditor.id}/update/', data = dict_toUpdateEditor)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')
        self.assertTrue(Editor.objects.filter(name = dict_toUpdateEditor['name']).first())

class EditorDeleteTest(TestCase):
    """ EditorDelete """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        self.obj_createdEditor, _ = Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'createdEditor',
                'sex': Editor.Sex.FEMALE,
            }
        )

    def test_001(self):
        """
        編集者の削除成功時に正しい URL へリダイレクトされるかどうか確認する
        """

        obj_response =  self.client.delete(f'/editors/{self.obj_createdEditor.id}/delete/')
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')
        self.assertFalse(Editor.objects.filter(name = self.obj_createdEditor.name).first())

class makeDictFromEditorsTest(TestCase):
    """ makeDictFromEditors """

    def setUp(self):
        self.dict_editors = []
        self.dict_editors.append(
            Editor.objects.create(
                name = 'male A',
                sex = Editor.Sex.MALE,
            )
        )
        self.dict_editors.append(
            Editor.objects.create(
                name = 'female A',
                sex = Editor.Sex.FEMALE,
            )
        )
        self.dict_editors.append(
            Editor.objects.create(
                name = 'sex unknown',
                sex = None,
            )
        )

    def test_001(self):
        """
        編集者リストを辞書配列化する
        """
        dict_expectedEditors = [
            {
                'id': 1,
                'name': 'male A',
                'sex': '男性'
            },
            {
                'id': 2,
                'name': 'female A',
                'sex': '女性'
            },
            {
                'id': 3,
                'name': 'sex unknown',
                'sex': ''
            },
        ]
        self.assertEqual(makeDictFromEditors(None, self.dict_editors), dict_expectedEditors)

class export_as_csvTest(TestCase):
    """ export_as_csv """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        
        Editor.objects.create(
            name = 'male A',
            sex = Editor.Sex.MALE,
        )
        Editor.objects.create(
            name = 'female A',
            sex = Editor.Sex.FEMALE,
        )
        Editor.objects.create(
            name = 'sex unknown',
            sex = None,
        )
        
    def test_001(self):
        """
        CSV 形式で出力されることを確認
        """
        obj_response = self.client.get('/editors/export_as_csv/')
        self.assertEqual(obj_response.status_code, 200)

        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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

        Editor.objects.create(
            name = 'male A',
            sex = Editor.Sex.MALE,
        )
        Editor.objects.create(
            name = 'female A',
            sex = Editor.Sex.FEMALE,
        )
        Editor.objects.create(
            name = 'sex unknown',
            sex = None,
        )

    def test_001(self):
        """
        CSVImputForm のバリデーションエラー
        """

        str_toImportCSVText = textwrap.dedent('''\
            ID,名前,性別
            4,"added, name",
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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
            ID,名前,性別
            4,"added, name",
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText.encode('shift-jis'))
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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
            ID,名前,性別
            4,added name,
            5.added name2,性
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
            4,added name,
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
            ID,名前,性別
            4,sex unknown,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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
            ID,名前,性別
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'replace',
        }

        obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
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
            ID,名前,性別
            4,added name,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'editors.views.Editor.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * (INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK - 1) +
                [Editor.objects.update_or_create(
                    id = 4,
                    defaults = {
                        'name': 'added name',
                        'sex': None
                    }
                )],
        ):
            obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
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
            ID,名前,性別
            4,added name,
        ''')
        # 改行 コードを `\r\n` に統一
        str_toImportCSVText = re.sub(r'\r\n', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\r', r'\n', str_toImportCSVText)
        str_toImportCSVText = re.sub(r'\n', r'\r\n', str_toImportCSVText)

        obj_csvfile = ContentFile(str_toImportCSVText)
        obj_csvfile.name = 'editors.csv'
        dict_toImportData = {
            'file': obj_csvfile,
            'mode': 'update',
        }

        with mock.patch(
            target = 'editors.views.Editor.objects.update_or_create',
            side_effect = 
                [OperationalError('database is locked')] * INT_TIMES_OF_RETRYING_CAUSE_OF_DEADLOCK,
        ):
            obj_response = self.client.post('/editors/import_from_csv/', data = dict_toImportData)

        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

        obj_response = self.client.get('/editors/export_as_csv/')
        
        str_expected = textwrap.dedent('''\
            ID,名前,性別
            1,male A,男性
            2,female A,女性
            3,sex unknown,
        ''')
        # 改行 コードを `\n` に統一
        str_expected = re.sub(r'\r\n', r'\n', str_expected)
        str_expected = re.sub(r'\r', r'\n', str_expected)

        str_behavior = obj_response.content.decode('utf-8-sig')
        str_behavior = re.sub(r'\r\n', r'\n', str_behavior)
        str_behavior = re.sub(r'\r', r'\n', str_behavior)
        self.assertEqual(str_behavior, str_expected)

class EditorCreateAPIViewTest(TestCase):
    """ EditorCreateAPIView """

    # TokenAPIViewForCreationTest で実施済みの観点のテストは省略

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = datetime.datetime.now() + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        名前の重複
        """
        Editor.objects.create(
            name = 'male A',
            sex = 'male',
        )
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "name": "male A",
                        "sex": "男性"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/editors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Editor が既に存在します。', status_code = 400)

    def test_002(self):
        """
        `sex` プロパティの未指定
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "name": "male A"
                    }
                ]
            }
        ''')
        obj_response = self.client.post(
            '/api/v1/editors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Editor.objects.filter(name = 'male A').first().sex, None)

class EditorListAPIViewTest(TestCase):
    """ EditorListAPIView """
    
    # TokenAPIViewForListTest で実施済みの観点のテストは省略

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = datetime.datetime.now() + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        クエリ文字列のバリデーション OK
        """

        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'maleA',
                'sex': Editor.Sex.MALE,
            }
        )
        self.obj_id2, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name':'femaleA',
                'sex': Editor.Sex.FEMALE,
            }
        )

        dict_expected = {
            'editors': [
                {
                    'id': 2,
                    'name': 'femaleA',
                    'sex': '女性',
                },
            ]
        }

        obj_response = self.client.get(f'/api/v1/editors.json/?id={self.obj_id2.id}&name={self.obj_id2.name}', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), dict_expected)

class EditorUpdateAPIViewTest(TestCase):
    """ EditorUpdateAPIView """

    # TokenAPIViewForUpdateTest で実施済みの観点のテストは省略

    def setUp(self):
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
        self.obj_token = TokenForRESTAPI.objects.create(
            user = obj_user,
            expired_date = datetime.datetime.now() + datetime.timedelta(days = 7) # 7 日加算
        )

    def test_001(self):
        """
        名前フィールドの重複
        """

        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name':'maleA',
                'sex': Editor.Sex.MALE,
            }
        )
        self.obj_id2, _ = Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name':'femaleA',
                'sex': Editor.Sex.FEMALE,
            }
        )
        str_input = textwrap.dedent(f'''\
            {{
                "editors": [
                    {{
                        "id": {self.obj_id2.id},
                        "name": "maleA"
                    }}
                ]
            }}
        ''')
        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'この 名前 を持った Editor が既に存在します。', status_code = 400)
