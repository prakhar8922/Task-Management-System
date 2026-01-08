from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, TaskAttachmentViewSet, CommentViewSet

app_name = 'tasks'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'attachments', TaskAttachmentViewSet, basename='attachment')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
