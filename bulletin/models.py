from uuid import uuid4
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

PENDING = 'PE'
ACCEPTED = 'AC'
REJECTED = 'RE'
PUB_STATUS = [
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected')
]


def picture_location(instance, filename, **kwargs):
    return f'pictures/image-{uuid4()}_{filename.split("/")[-1]}'


def audio_location(instance, filename, **kwargs):
    return f'audios/audio-{uuid4()}_{filename.split("/")[-1]}'


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_('created_at'), default=now)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    posted_at = models.DateTimeField(default=None, null=True)
    published_status = models.CharField(max_length=2, choices=PUB_STATUS, null=False, default=PENDING)

    class Meta:
        abstract = True


class Comment(CommonInfo):
    author = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField()
    audio = models.FileField(upload_to=audio_location, null=True, default=None)
    sentiment = models.JSONField(default=dict)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "comments"

    def get_accepted_comments(self):
        return self.objects.filter(published_status=ACCEPTED)


class Picture(CommonInfo):
    uploader = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=500, null=False, blank=False)
    image = models.ImageField(_('main picture'), upload_to=picture_location, null=False)
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id', related_query_name='picture')

    def __str__(self):
        return self.image.name.split('/')[-1]


class Story(CommonInfo):
    author = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=500, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    sentiment = models.JSONField(default=dict)
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id', related_query_name='story')
    audio = models.FileField(upload_to=audio_location, null=True, default=None)

    def __str__(self):
        return f'{self.author}:{self.title}'

    class Meta:
        verbose_name_plural = "stories"
