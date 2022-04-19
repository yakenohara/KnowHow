from django.db.models import Q

from rest_framework import serializers

from .models import Author

class AuthorSerializerForQueryString(serializers.Serializer):

    id = serializers.IntegerField(required = False)
    name = serializers.CharField(required = False)

    def getQueryDictForFilter(self):
        dict_queryForFilter = {}

        for str_fieldName in ['id','name']:
            if self.validated_data.get(str_fieldName):
                dict_queryForFilter[str_fieldName] = self.validated_data.get(str_fieldName)
        
        return dict_queryForFilter

class AuthorSerializerForCreate(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 255)
    birthday = serializers.DateField(required = False, allow_null = True)

    class Meta:
        model = Author
        fields = (
            'name',
            'birthday',
        )

    def validate(self, data):

        if Author.objects.filter(name = data.get('name')).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Author が既に存在します。')

        data['birthday'] = data.get('birthday', None)
        
        return data

class AuthorSerializerForUpdate(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 255)
    birthday = serializers.DateField(required = False, allow_null = True)

    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, data):

        # 別レコードですでに使われている名前かどうかチェック
        if Author.objects.filter(
            ~Q(id = data.get('id')) &
            Q(name = data.get('name'))
        ).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Author が既に存在します。')

        data['birthday'] = data.get('birthday', None)
        
        return data
