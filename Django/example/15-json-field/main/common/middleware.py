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
