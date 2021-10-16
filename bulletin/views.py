from rest_framework import mixins, viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView

from bulletin import models
from bulletin import serializers


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.CommentDetailSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(published_status=models.ACCEPTED).all()


class StoryViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StoryListSerializer
        return serializers.StoryDetailSerializer

    def get_queryset(self):
        return models.Story.objects.filter(published_status=models.ACCEPTED).all()

    @action(detail=False, methods=['get'])
    def count(self, request, pk=None):
        count = models.Story.objects.filter(published_status=models.ACCEPTED).count()
        return Response({'count': count}, status=status.HTTP_200_OK)


class PictureViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PictureListSerializer
        return serializers.PictureDetailSerializer

    def get_queryset(self):
        return models.Picture.objects.filter(published_status=models.ACCEPTED).all()

    @action(detail=False, methods=['get'])
    def count(self, request, pk=None):
        count = models.Picture.objects.filter(published_status=models.ACCEPTED).count()
        return Response({'count': count}, status=status.HTTP_200_OK)


class ContentTypeInfo(APIView):
    def get(self, request, format=None):
        picture_content_type = ContentType.objects.get_for_model(models.Picture)
        story_content_type = ContentType.objects.get_for_model(models.Story)
        return Response({
            'picture': picture_content_type.id,
            'story': story_content_type.id,
        }, status=status.HTTP_200_OK)
