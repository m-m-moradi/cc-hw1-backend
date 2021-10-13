from rest_framework import serializers
from generic_relations.relations import GenericRelatedField
from .models import *


class CommentDetailSerializer(serializers.ModelSerializer):
    content_object = GenericRelatedField({
        Picture: serializers.PrimaryKeyRelatedField(queryset=Picture.objects.all()),
        Story: serializers.PrimaryKeyRelatedField(queryset=Story.objects.all()),
    })

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at',
            'posted_at',
        ]


class PictureListSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Picture
        fields = [
            'id',
            'image',
            'created_at',
            'updated_at'
        ]


class PictureDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Picture
        fields = [
            'id',
            'image',
        ]
        read_only_fields = [
            'created_at',
            'updated_at'
        ]


class StoryListSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'file',
            'created_at',
            'updated_at'
        ]


class StoryDetailSerializer(serializers.ModelSerializer):
    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'file',
        ]
        read_only_fields = [
            'created_at',
            'updated_at'
        ]
