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
        str_errmsg = f'Specified {self.model.__name__} ID: {pk} not found.'
        logger.warning(str_errmsg)
        return Response({'detail': str_errmsg}, status=status.HTTP_404_NOT_FOUND)

# ここ以降に Open API 準拠の API ドキュメント用定義を記載する

from rest_framework import serializers

class InvalidReasonSerializerForDoc(serializers.Serializer):
    detail = serializers.CharField(help_text = 'エラーメッセージ')
