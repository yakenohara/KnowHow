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
