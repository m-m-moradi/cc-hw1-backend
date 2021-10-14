from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from bulletin import models


class CommentDetailSerializer(serializers.ModelSerializer):
    content_object = GenericRelatedField({
        models.Picture: serializers.PrimaryKeyRelatedField(queryset=models.Picture.objects.all()),
        models.Story: serializers.PrimaryKeyRelatedField(queryset=models.Story.objects.all()),
    }, read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at',
            'posted_at',
        ]


class PictureListSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Picture
        fields = '__all__'


class PictureDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Picture
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at'
        ]


class StoryListSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Story
        fields = '__all__'


class StoryDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Story
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at'
        ]
