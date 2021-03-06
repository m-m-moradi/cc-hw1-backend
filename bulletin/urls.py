from django.urls import path
from rest_framework.routers import DefaultRouter
from bulletin import views

urlpatterns = [
    path('content_type/', views.ContentTypeInfo.as_view(), name="content_type_info"),
]

router = DefaultRouter()

router.register('stories', views.StoryViewSet, basename='stories')
router.register('pictures', views.PictureViewSet, basename='pictures')
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns += router.urls
