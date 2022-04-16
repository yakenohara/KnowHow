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
