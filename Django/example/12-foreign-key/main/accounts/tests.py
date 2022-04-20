import json

from django.contrib.auth.models import User
from django.test import TestCase

from json.decoder import JSONDecodeError

from .models import TokenForRESTAPI

# Create your tests here.

class CreateViewTest(TestCase):
    """ CreateView """

    def test_001(self):
        """
        使用しているテンプレートファイルが正しいかどうかを確認する
        """

        # /accounts/create にアクセス
        obj_response =  self.client.get('/accounts/signup/')
        
        # 使用しているテンプレートファイルが 'accounts/form.html' であるかどうかをチェックする
        self.assertTemplateUsed(obj_response, 'accounts/form.html')

    def test_002(self):
        """
        アカウント作成に成功した時に、'/' へリダイレクトされることを確認する
        """
        dict_toCreateAccount = {
            'username': 'user1',
            'password1': 'supersuper', # パスワードの設定
            'password2': 'supersuper', # 確認用パスワードの設定
        }
        obj_response = self.client.post('/accounts/signup/', data = dict_toCreateAccount)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/')

class LoginViewTest(TestCase):
    """ LoginView """

    def test_001(self):
        """
        ログインページにアクセスする認証済みユーザーが、ログインに成功したかのようにリダイレクトされるかどうか確認
        """
        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)

        obj_response =  self.client.get('/accounts/login/?next=/editors/')
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/editors/')

    def test_002(self):
        """
        ログインページにで使用されるテンプレートファイルが正しいかどうか確認する
        """
        obj_response =  self.client.get('/accounts/login/')
        self.assertTemplateUsed(obj_response, 'accounts/login.html')

class AccountCreateViewTest(TestCase):
    """ AccountCreateView """

    def setUp(self):
    # この関数は各テスト関数の実施の直前に毎回コールされる

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
    
    def test_001(self):
        """
        使用しているテンプレートファイルが正しいかどうかを確認する
        """

        obj_response =  self.client.get('/accounts/create/')
        self.assertTemplateUsed(obj_response, 'accounts/form.html')

    def test_002(self):
        """
        アカウント作成に成功した時に、'/accounts/' へリダイレクトされることを確認する
        """
        dict_toCreateAccount = {
            'username': 'user1',
            'password1': 'supersuper', # パスワードの設定
            'password2': 'supersuper', # 確認用パスワードの設定
        }
        obj_response = self.client.post('/accounts/create/', data = dict_toCreateAccount)
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/accounts/')
        
class AccountsListViewTest(TestCase):
    """ AccountsListView """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
    
    def test_001(self):
        """
        使用しているテンプレートファイルが正しいかどうかを確認する
        """
        obj_response =  self.client.get('/accounts/')
        self.assertTemplateUsed(obj_response, 'accounts/list.html')

class AccountDeleteTest(TestCase):
    """ AccountDelete """

    def setUp(self):

        # Force Login
        obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(obj_user)
    
    def test_001(self):
        """
        ユーザー削除成功時に、'/accounts/' へリダイレクトされることを確認する
        """

        obj_toDeleteUser = User.objects.create_user(
            username = 'deluser',
            password = '0123'
        )
        obj_response =  self.client.post(f'/accounts/{obj_toDeleteUser.id}/delete/')
        self.assertEqual(obj_response.status_code, 302)
        self.assertEqual(obj_response.url, '/accounts/')

class createTokenTest(TestCase):
    """ createToken """

    def setUp(self):

        # Force Login
        self.obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(self.obj_user)

    def test_001(self):
        """
        GET method でアクセスした際に使用しているテンプレートファイルが正しいかどうかを確認する
        """

        obj_response =  self.client.get(f'/accounts/{self.obj_user.id}/token/create/')
        self.assertTemplateUsed(obj_response, 'accounts/form_token.html')

    def test_002(self):
        """
        valid なデータ(有効期限 1 週間)を POST した際にトークンが返却されることを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.ONE_WEEK.value
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id}/token/create/', dict_formForCreateToken)
        self.assertTrue('token' in json.loads(obj_response.content))

    def test_003(self):
        """
        valid なデータ(有効期限 1 ヶ月)を POST した際にトークンが返却されることを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.ONE_MONTH.value
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id}/token/create/', dict_formForCreateToken)
        self.assertTrue('token' in json.loads(obj_response.content))

    def test_004(self):
        """
        valid なデータ(有効期限 3 ヶ月)を POST した際にトークンが返却されることを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.THREE_MONTHS.value
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id}/token/create/', dict_formForCreateToken)
        self.assertTrue('token' in json.loads(obj_response.content))

    def test_005(self):
        """
        valid なデータ(有効期限なし)を POST した際にトークンが返却されることを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.NO_EXPIRATION.value
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id}/token/create/', dict_formForCreateToken)
        self.assertTrue('token' in json.loads(obj_response.content))

    def test_006(self):
        """
        invalid なデータを POST した際にトークンが返却されないことを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.ONE_WEEK
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id}/token/create/', dict_formForCreateToken)
        bl_jsonDecodeErr = False
        try:
            json.loads(obj_response.content)
        except JSONDecodeError: # JSON でない場合
            bl_jsonDecodeErr = True
        
        self.assertTrue(bl_jsonDecodeErr)

    def test_007(self):
        """
        トークン生成対象のユーザーが存在しない場合に 404 が返却されることを確認する
        """
        dict_formForCreateToken = {
            'expiration': TokenForRESTAPI.Expiration.NO_EXPIRATION.value
        }
        obj_response =  self.client.post(f'/accounts/{self.obj_user.id + 1}/token/create/', dict_formForCreateToken)
        self.assertEqual(obj_response.status_code, 404)

class deleteTokenTest(TestCase):
    """ deleteToken """

    def setUp(self):

        # Force Login
        self.obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(self.obj_user)

    def test_001(self):
        """
        トークン削除成功時にユーザー一覧へリダイレクトされることを確認
        """

        obj_response =  self.client.get(f'/accounts/{self.obj_user.id}/token/delete/')
        self.assertEqual(obj_response.status_code, 302)

    def test_004(self):
        """
        トークン削除対象のユーザーが存在しない場合に 404 を返すことを確認
        """

        obj_response =  self.client.get(f'/accounts/{self.obj_user.id + 1}/token/delete/')
        self.assertEqual(obj_response.status_code, 404)
