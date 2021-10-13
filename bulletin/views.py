from rest_framework import mixins, viewsets, generics
from bulletin import models
from bulletin import serializers


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = models.Story.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StoryListSerializer
        return serializers.StoryDetailSerializer


class PictureViewSet(viewsets.ModelViewSet):
    queryset = models.Picture.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PictureListSerializer
        return serializers.PictureDetailSerializer
