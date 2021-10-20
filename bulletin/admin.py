from django.contrib import admin
from .models import *


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'posted_at', 'audio', 'sentiment']
    list_filter = ['created_at', 'updated_at', 'posted_at']
    list_display = ['id', 'author', 'published_status']
    search_fields = ['title', 'id']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'posted_at', 'audio', 'sentiment']
    list_filter = ['created_at', 'updated_at', 'posted_at']
    list_display = ['id', 'author', 'published_status', 'title']
    search_fields = ['title', 'id']


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at', 'posted_at']
    list_filter = ['created_at', 'updated_at', 'posted_at']
    list_display = ['id', 'uploader', 'published_status', 'title']
    search_fields = ['title', 'id']
