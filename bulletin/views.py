from tempfile import TemporaryFile

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import TextToSpeechV1, ApiException
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from bulletin import models, serializers


def perform_create_get_sentiment(view, serializer):
    authenticator = IAMAuthenticator(settings.IBM_NLP_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(settings.IBM_NLP_API_URL)
    response = natural_language_understanding.analyze(
        text=serializer.validated_data['text'],
        features=Features(sentiment=SentimentOptions())).get_result()

    serializer.validated_data['sentiment'] = response
    if response['sentiment']['document']['score'] < -0.5:
        serializer.validated_data['published_status'] = models.REJECTED
    serializer.save()


# noinspection PyUnresolvedReferences
class TextToSpeechMixin(object):
    @action(detail=True, methods=['get'])
    def audio(self, request, pk=None):
        api_key = settings.IBM_T2S_API_KEY
        url = settings.IBM_T2S_API_URL
        authenticator = IAMAuthenticator(api_key)
        text_to_speech = TextToSpeechV1(
            authenticator=authenticator
        )
        text_to_speech.set_service_url(url)

        item = self.get_object()
        item_type_name = self.get_queryset().model.__name__

        if item.audio:
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            with TemporaryFile('wb+') as audio_file:
                audio_file.write(
                    text_to_speech.synthesize(
                        item.text,
                        voice='en-US_AllisonV3Voice',
                        accept='audio/wav'
                    ).get_result().content)
                item.audio.save(f'{item_type_name}-{item.id}.wav', File(audio_file))

            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection PyUnresolvedReferences
class SentimentMixin(object):
    @action(detail=True, methods=['get'])
    def sentiment(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item)

        if item.sentiment:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            authenticator = IAMAuthenticator(settings.IBM_NLP_API_KEY)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version='2021-08-01',
                authenticator=authenticator
            )

            natural_language_understanding.set_service_url(settings.IBM_NLP_API_URL)
            response = natural_language_understanding.analyze(
                text=item.text,
                features=Features(sentiment=SentimentOptions())).get_result()

            item.sentiment = response
            item.save()
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(TextToSpeechMixin,
                     SentimentMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.CommentDetailSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(published_status=models.ACCEPTED).all()

    def perform_create(self, serializer):
        perform_create_get_sentiment(self, serializer)

    def perform_update(self, serializer):
        perform_create_get_sentiment(self, serializer)


class StoryViewSet(TextToSpeechMixin, SentimentMixin, viewsets.ModelViewSet):

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

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        story = self.get_object()
        comments = models.Comment.objects.filter(story=story, published_status=models.ACCEPTED)
        serializer = serializers.CommentDetailSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        perform_create_get_sentiment(self, serializer)

    def perform_update(self, serializer):
        perform_create_get_sentiment(self, serializer)


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

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        picture = self.get_object()
        comments = models.Comment.objects.filter(picture=picture, published_status=models.ACCEPTED)
        serializer = serializers.CommentDetailSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContentTypeInfo(APIView):
    def get(self, request, format=None):
        picture_content_type = ContentType.objects.get_for_model(models.Picture)
        story_content_type = ContentType.objects.get_for_model(models.Story)
        return Response({
            'picture': picture_content_type.id,
            'story': story_content_type.id,
        }, status=status.HTTP_200_OK)
