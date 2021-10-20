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
            'sentiment',
            'audio',
            'created_at',
            'updated_at',
            'posted_at',
        ]


# noinspection PyMethodMayBeStatic
class PictureListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = models.Picture
        fields = '__all__'

    def get_comments(self, picture):
        items = models.Comment.objects.filter(picture=picture, published_status=models.ACCEPTED)
        return [obj.id for obj in items]


# noinspection PyMethodMayBeStatic
class PictureDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = models.Picture
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at'
        ]

    def get_comments(self, picture):
        items = models.Comment.objects.filter(picture=picture, published_status=models.ACCEPTED)
        serializer = CommentDetailSerializer(instance=items, many=True)
        return serializer.data


# noinspection PyMethodMayBeStatic
class StoryListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = models.Story
        fields = '__all__'

    def get_comments(self, story):
        items = models.Comment.objects.filter(story=story, published_status=models.ACCEPTED)
        return [obj.id for obj in items]


# noinspection PyMethodMayBeStatic
class StoryDetailSerializer(serializers.ModelSerializer):
    # comments = CommentDetailSerializer(many=True, read_only=True, source='get_accepted_comments')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = models.Story
        fields = '__all__'
        read_only_fields = [
            'sentiment',
            'audio',
            'created_at',
            'updated_at'
        ]

    def get_comments(self, story):
        items = models.Comment.objects.filter(story=story, published_status=models.ACCEPTED)
        serializer = CommentDetailSerializer(instance=items, many=True)
        return serializer.data
