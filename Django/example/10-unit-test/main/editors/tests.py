import textwrap

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.test import TestCase

from editors.models import Editor
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
        dict_editors = []
        dict_editors.append(
            Editor.objects.create(
                name = 'male A',
                sex = Editor.Sex.MALE,
            )
        )
        dict_editors.append(
            Editor.objects.create(
                name = 'female A',
                sex = Editor.Sex.FEMALE,
            )
        )
        dict_editors.append(
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
        self.assertEqual(makeDictFromEditors(None, Editor.objects.all()), dict_expectedEditors)

# todo export_as_csv

class import_from_csvTest(TestCase):
    """ import_from_csv """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

    def test001(self):
        text = textwrap.dedent('''\
            ID,名前,性別
            1,updatename,女性\
        '''
        )

        print(text)

        csvfile = ContentFile(text)
        csvfile.name = 'to_import_csv.csv'
        data = {
            'file': csvfile,
            'mode': 'update',
        }
