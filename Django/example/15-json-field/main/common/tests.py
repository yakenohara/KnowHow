import csv
import datetime
import io
import json
import textwrap

from unittest import mock

from django.contrib.auth.models import User
from django.db.utils import OperationalError
from django.test import TestCase
from django.test import TransactionTestCase
from django.utils.timezone import make_aware

from accounts.models import TokenForRESTAPI
from editors.models import Editor

from common.const import STR_ATTRIBUTE_KEYWORD_FOR_TOKEN
from common.utilities import StrChoiceEnum, makeVerboseNameVsFieldNameDict, makeCSVStringFromDict, getOrdinalString, getQeryStringInURL, parseCommaSeparatedList

# <auth.py>--------------------------------------------------------------------

class TokenAuthenticationForRESTAPITest(TestCase):
    """
    TokenAuthenticationForRESTAPI
    TokenAPIView
    """

    def setUp(self):
        # Force Login
        self.obj_user = User.objects.create_user(
            username = 'tester',
            password = '0123'
        )
        self.client.force_login(self.obj_user)

    def test_001(self):
        """
        トークン期限内
        """
        obj_token = TokenForRESTAPI.objects.create(
            user = self.obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = 7) # 7 日加算
        )

        obj_response = self.client.get('/api/v1/editors.json/', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {obj_token.key}')
        self.assertEqual(obj_response.status_code, 200)
    
    def test_002(self):
        """
        トークン期限切れ
        """
        obj_token = TokenForRESTAPI.objects.create(
            user = self.obj_user,
            expired_date = make_aware(datetime.datetime.now()) + datetime.timedelta(days = -7) # 7 日減算
        )

        obj_response = self.client.get('/api/v1/editors.json/', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {obj_token.key}')
        dict_expected = {"detail":"認証トークンの期限切れです。"}
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), dict_expected)

# -------------------------------------------------------------------</auth.py>

# <utilities.py>---------------------------------------------------------------

class makeChoiceEnumTest(TestCase):
    """ makeChoiceEnum """
    
    def test_001(self):
        """
        クラスに定義された 2 つの要素をもったタプルが意図通り返却されることを確認する
        """

        class TestCls(StrChoiceEnum):
            A = ('a', 'あ')
            B = ('b', 'い')
            C = ('c', 'う')

        lst_expected = [('a', 'あ'), ('b', 'い'), ('c', 'う')]
        lst_reversedExpected = [('あ', 'a'), ('い', 'b'), ('う', 'c')]

        self.assertEqual(TestCls.choices(), lst_expected)
        self.assertEqual(TestCls.reversedChoices(), lst_reversedExpected)

class makeVerboseNameVsFieldNameDictTest(TestCase):
    """ makeVerboseNameVsFieldNameDict """

    def test_001(self):
        """
        モデルから verbose_name とフィールド名の対応表を作成して返すかどうかを確認する
        """
        dict_expected = {
            'ID': 'id',
            '名前': 'name',
            '性別': 'sex',
        }
        self.assertEqual(makeVerboseNameVsFieldNameDict(Editor), dict_expected)

class makeCSVStringFromDictTest(TestCase):
    """ makeCSVStringFromDict """

    def test_001(self):
        """
        モデルを辞書配列化したものを CSV 文字列化していることを確認する
        """
        dict_editors = [
            {
                'name': 'test1',
                'sex':  None,
            },
            {
                'name': 'test2',
                'sex':  'male',
            },
        ]
        str_columDefs = ['id', 'name', 'sex']

        with io.StringIO() as stream:
 
            writer = csv.writer(stream)
            writer.writerow(str_columDefs)

            for dict_model in dict_editors:
                writer.writerow(dict_model.values())
    
            # BOM 付き UTF-8 文字列を取得 
            str_expected = stream.getvalue().encode('utf-8-sig') 

        self.assertEqual(makeCSVStringFromDict(dict_editors, str_columDefs), str_expected)

class getOrdinalStringTest(TestCase):
    """ getOrdinalString """

    def test_001(self):
        """
        数値を正しい序数詞 (1st, 2nd, 3rd 等) に変換しているかどうか確認
        """
        str_expected = [
            '1st',
            '2nd',
            '3rd',
            '4th',
            '5th',
            '6th',
            '7th',
            '8th',
            '9th',
            '10th',
            '11th',
            '12th',
            '13th',
            '14th',
            '15th',
            '16th',
            '17th',
            '18th',
            '19th',
            '20th',
            '21st',
            '22nd',
            '23rd',
            '24th',
        ]
        str_behavior = [ getOrdinalString(i + 1) for i in range(24)]

        self.assertEqual(str_behavior, str_expected)

class getQeryStringInURLTest(TestCase):
    """ getQeryStringInURL """

    def test_001(self):
        """
        ディクショナリ化されたクエリ文字列 (クエリストリング) を元に戻しているかどうか確認
        """
        dict_query = {
            'id': 1,
            'name': 'Foo Bar',
        }
        str_expected = '?id=1&name=Foo%20Bar'
        self.assertEqual(getQeryStringInURL(dict_query), str_expected)

class parseCommaSeparatedListTest(TestCase):
    """ parseCommaSeparatedList """

    def test_001(self):
        """
        空文字列の指定
        """
        str_expected = []
        int_expected = -1

        str_behavior, int_behavior = parseCommaSeparatedList('')

        self.assertEqual(str_behavior, str_expected)
        self.assertEqual(int_behavior, int_expected)

    def test_002(self):
        """
        エスケープされた '\' と ','
        """
        str_expected = ['\\', ',']
        int_expected = -1

        str_behavior, int_behavior = parseCommaSeparatedList('\\\\,\,')

        self.assertEqual(str_behavior, str_expected)
        self.assertEqual(int_behavior, int_expected)

    def test_003(self):
        """
        直前の文字がエスケープ文字 '\' なのに、当該文字が '\' でも ',' でもない場合
        """

        str_expected = []
        int_expected = 1

        str_behavior, int_behavior = parseCommaSeparatedList('\\a')

        self.assertEqual(str_behavior, str_expected)
        self.assertEqual(int_behavior, int_expected)

    def test_004(self):
        """
        最後の文字が '\' の場合
        """

        str_expected = []
        int_expected = 1

        str_behavior, int_behavior = parseCommaSeparatedList('a\\')

        self.assertEqual(str_behavior, str_expected)
        self.assertEqual(int_behavior, int_expected)

    def test_005(self):
        """
        様々なパターン
        """

        str_expected = ['', ',', '\\', '']
        int_expected = -1

        str_behavior, int_behavior = parseCommaSeparatedList(',\,,\\\\,')

        self.assertEqual(str_behavior, str_expected)
        self.assertEqual(int_behavior, int_expected)

        
# ---------------------------------------------------------------<utilities.py>

# <views.py>-------------------------------------------------------------------

class TokenAPIViewForCreationTest(TestCase):
    """
    TokenAPIViewForCreation
    EditorCreateAPIView
    """

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
        JSON ファイルのパースエラー
        """
        str_input = textwrap.dedent('''\
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
            
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'JSONDecodeError occured while `json.loads`. Check following.', status_code = 400)

    def test_002(self):
        """
        パースしたデータが辞書型でない
        """
        str_input = textwrap.dedent('''\
            [
                "a","b","c"
            ]
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Unexpected format:', status_code = 400)

    def test_003(self):
        """
        あらかじめ定めておいたプロパティ名で定義された値が list でない
        """
        str_input = textwrap.dedent('''\
            {
                "ditors": [
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
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/create/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Unexpected format:', status_code = 400)

    def test_004(self):
        """
        バリデーションエラー
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "name": "sex unknown",
                        "sex": "性"
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
        self.assertContains(obj_response, 'は有効な選択肢ではありません。', status_code = 400)

    def test_005(self):
        """
        デッドロックの発生
        """
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

        with mock.patch(
            target = 'editors.serializer.EditorSerializerForCreate.save',
            side_effect = [
                OperationalError('database is locked')
            ],
        ):

            obj_response = self.client.post(
                '/api/v1/editors/create/',
                HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
                data = str_input,
                content_type = 'application/json',
            )

        self.assertContains(obj_response, 'database is locked', status_code = 500)

    def test_006(self):
        """
        レコード保存成功
        """
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
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(Editor.objects.filter(id = 1).first().name, 'male A')

class TokenAPIViewForListTest(TransactionTestCase):
    """
    TokenAPIViewForList
    EditorListAPIView
    """

    reset_sequences = True

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

        Editor.objects.create(
            name = 'male A',
            sex = 'male',
        )
        Editor.objects.create(
            name = 'female A',
            sex = 'female',
        )

        dict_expected = {
            'editors': [
                {
                    'id': 1,
                    'name': 'male A',
                    'sex': '男性',
                },
                {
                    'id': 2,
                    'name': 'female A',
                    'sex': '女性',
                },
            ]
        }

        obj_response = self.client.get('/api/v1/editors.json/', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(obj_response.status_code, 200)
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), dict_expected)

    def test_002(self):
        """
        クエリ文字列のバリデーション NG
        """
        obj_response = self.client.get('/api/v1/editors.json/?id=a', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertContains(obj_response, 'Validation error found in', status_code = 400)

class TokenAPIViewForUpdateTest(TestCase):
    """
    TokenAPIViewForUpdate
    EditorUpdateAPIView
    """

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
        
        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'male A',
                'sex': 'male',
            }
        )
        Editor.objects.update_or_create(
            id = 2,
            defaults = {
                'name': 'female A',
                'sex': 'female',
            }
        )
        Editor.objects.update_or_create(
            id = 3,
            defaults = {
                'name': 'sex unknown',
                'sex': None,
            }
        )

    def test_001(self):
        """
        JSON ファイルのパースエラー
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated",
                    }
                ]
            
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'JSONDecodeError occured while `json.loads`. Check following.', status_code = 400)

    def test_002(self):
        """
        パースしたデータが辞書型でない
        """
        str_input = textwrap.dedent('''\
            [
                "a","b","c"
            ]
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Unexpected format:', status_code = 400)

    def test_003(self):
        """
        あらかじめ定めておいたプロパティ名で定義された値が list でない
        """
        str_input = textwrap.dedent('''\
            {
                "ditors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Unexpected format:', status_code = 400)

    def test_004(self):
        """
        `id` プロパティが存在しない場合
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Validation error: property `id` not found in ', status_code = 400)

    def test_005(self):
        """
        指定 `id` が存在しない場合
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 4,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, '見つかりませんでした。', status_code = 404)

    def test_006(self):
        """
        デッドロックの発生
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        with mock.patch(
            target = 'editors.serializer.EditorSerializerForUpdate.save',
            side_effect = [
                OperationalError('database is locked')
            ],
        ):

            obj_response = self.client.post(
                '/api/v1/editors/update/',
                HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
                data = str_input,
                content_type = 'application/json',
            )

        self.assertContains(obj_response, 'database is locked', status_code = 500)

    def test_007(self):
        """
        バリデーション OK
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertEqual(obj_response.status_code, 200)

        str_expected = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "男性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated",
                        "sex": ""
                    }
                ]
            }
        ''')

        obj_response = self.client.get('/api/v1/editors.json/', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), json.loads(str_expected))

    def test_008(self):
        """
        バリデーション NG
        """
        str_input = textwrap.dedent('''\
            {
                "editors": [
                    {
                        "id": 1,
                        "name": "male updated",
                        "sex": "性"
                    },
                    {
                        "id": 2,
                        "name": "female updated",
                        "sex": "女性"
                    },
                    {
                        "id": 3,
                        "name": "sex unknown updated"
                    }
                ]
            }
        ''')

        obj_response = self.client.post(
            '/api/v1/editors/update/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            data = str_input,
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'は有効な選択肢ではありません。', status_code = 400)

class TokenAPIViewForDeletionTest(TestCase):
    """
    TokenAPIViewForDeletion
    EditorDeleteAPIView
    """

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

        Editor.objects.update_or_create(
            id = 1,
            defaults = {
                'name': 'male A',
                'sex': 'male',
            }
        )

    def test_001(self):
        """
        削除対象オブジェクトが存在する場合
        """
        obj_response = self.client.delete(
            '/api/v1/editors/1/delete/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            content_type = 'application/json',
        )

        self.assertEqual(obj_response.status_code, 200)

        str_expected = textwrap.dedent('''\
            {
                "editors": []
            }
        ''')

        obj_response = self.client.get('/api/v1/editors.json/', HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}')
        self.assertEqual(json.loads(obj_response.content.decode('utf-8')), json.loads(str_expected))

    def test_002(self):
        """
        削除対象オブジェクトが存在しない場合
        """
        obj_response = self.client.delete(
            '/api/v1/editors/2/delete/',
            HTTP_AUTHORIZATION = f'{STR_ATTRIBUTE_KEYWORD_FOR_TOKEN} {self.obj_token.key}',
            content_type = 'application/json',
        )
        self.assertContains(obj_response, 'Specified Editor ID: 2 not found.', status_code = 404)

# ------------------------------------------------------------------</views.py>