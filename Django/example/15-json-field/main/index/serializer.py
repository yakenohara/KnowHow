from django.db.models import Q

from rest_framework import serializers

from authors.models import Author

from editors.models import Editor

from .models import Book

class BookSerializerForQueryString(serializers.Serializer):

    id = serializers.IntegerField(required = False)
    name = serializers.CharField(required = False)

    def getQueryDictForFilter(self):
        dict_queryForFilter = {}

        for str_fieldName in ['id','name']:
            if self.validated_data.get(str_fieldName):
                dict_queryForFilter[str_fieldName] = self.validated_data.get(str_fieldName)
        
        return dict_queryForFilter

class WordListingField(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class BookSerializerForCreate(serializers.ModelSerializer):
    name = serializers.CharField(max_length = 255)
    author = serializers.CharField(max_length = 255, required = False, allow_blank = True)
    editors = WordListingField(many = True, required = False)

    class Meta:
        model = Book
        fields = (
            'name',
            'author',
            'editors',
        )

    def validate(self, data):

        if Book.objects.filter(name = data.get('name')).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Book が既に存在します。')

        str_author = data.get('author', None)
        if str_author: # 著者が指定されている場合
            obj_toSaveAuthor = Author.objects.filter(name = str_author).first()
            if not obj_toSaveAuthor: # 存在しない著者名の場合
                raise serializers.ValidationError(f'指定された著者名 `{str_author}` は存在しません。')
            data['author'] = obj_toSaveAuthor
        else: # 著者が指定されていない場合
            data['author'] = None

        str_editors = data.get('editors', None)
        if str_editors: # 編集者が指定されている場合
            int_toSaveEditorIDs = []
            for str_editor in str_editors:
                obj_toSaveEditor = Editor.objects.filter(name = str_editor).first()
                if not obj_toSaveEditor: # 存在しない編集者の場合
                    raise serializers.ValidationError(f'指定された編集者名 `{str_editor}` は存在しません。')
                int_toSaveEditorIDs.append(obj_toSaveEditor.id)

            data['editors'] = int_toSaveEditorIDs

        else: # 編集者が指定されていない場合
            data['editors'] = []

        return data

    # https://www.django-rest-framework.org/community/3.0-announcement/#the-create-and-update-methods
    def create(self, validated_data):
        
        int_toSaveEditorIDs = validated_data.pop('editors')
        obj_createdBook = super().create(validated_data)
        obj_createdBook.editors.set(int_toSaveEditorIDs)

        return obj_createdBook

class BookSerializerForUpdate(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 255)
    author = serializers.CharField(max_length = 255, required = False, allow_blank = True)
    editors = WordListingField(many = True, required = False)

    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, data):

        # 別レコードですでに使われている名前かどうかチェック
        if Book.objects.filter(
            ~Q(id = data.get('id')) &
            Q(name = data.get('name'))
        ).first(): # すでに登録済みの名前の場合
            raise serializers.ValidationError('この 名前 を持った Book が既に存在します。')

        str_author = data.get('author', None)
        if str_author: # 著者が指定されている場合
            obj_toSaveAuthor = Author.objects.filter(name = str_author).first()
            if not obj_toSaveAuthor: # 存在しない著者名の場合
                raise serializers.ValidationError(f'指定された著者名 `{str_author}` は存在しません。')
            data['author'] = obj_toSaveAuthor
        else: # 著者が指定されていない場合
            data['author'] = None

        str_editors = data.get('editors', None)
        if str_editors: # 編集者が指定されている場合
            int_toSaveEditorIDs = []
            for str_editor in str_editors:
                obj_toSaveEditor = Editor.objects.filter(name = str_editor).first()
                if not obj_toSaveEditor: # 存在しない編集者の場合
                    raise serializers.ValidationError(f'指定された編集者名 `{str_editor}` は存在しません。')
                int_toSaveEditorIDs.append(obj_toSaveEditor.id)

            data['editors'] = int_toSaveEditorIDs

        else: # 編集者が指定されていない場合
            data['editors'] = []
        
        return data

    # https://www.django-rest-framework.org/community/3.0-announcement/#the-create-and-update-methods
    def update(self, instance, validated_data):
        
        int_toSaveEditorIDs = validated_data.pop('editors')        
        super().update(instance, validated_data)
        instance.editors.set(int_toSaveEditorIDs)

        return instance
