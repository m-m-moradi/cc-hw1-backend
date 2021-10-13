from uuid import uuid4
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


def picture_location(instance, filename, **kwargs):
    return f'pictures/image-{uuid4()}_{filename.split("/")[-1]}'


def story_location(instance, filename, **kwargs):
    return f'stories/story-{uuid4()}_{filename.split("/")[-1]}'


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_('created_at'), default=now)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        abstract = True


class Comment(CommonInfo):
    PENDING = 'PE'
    ACCEPTED = 'AC'
    REJECTED = 'RE'
    PUB_STATUS = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    ]
    author = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    date_posted = models.DateTimeField(default=now, null=True)
    published_status = models.CharField(max_length=2, choices=PUB_STATUS, null=False, default=PENDING)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "comments"


class Picture(CommonInfo):
    image = models.ImageField(_('main picture'), upload_to=picture_location, null=False)
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')

    def __str__(self):
        return self.image.name.split('/')[-1]


class Story(CommonInfo):
    file = models.FileField(_('story file'), upload_to=story_location, null=False)
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')

    def __str__(self):
        return self.file.name.split('/')[-1]

    class Meta:
        verbose_name_plural = "stories"
