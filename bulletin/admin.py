from django.contrib import admin
from .models import *


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
