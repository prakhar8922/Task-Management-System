from django.contrib import admin
from .models import Task, Tag, TaskAttachment, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model"""
    list_display = ('name', 'color', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model"""
    list_display = ('title', 'project', 'status', 'priority', 'created_by', 'created_at')
    list_filter = ('status', 'priority', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'project__title', 'created_by__email')
    filter_horizontal = ('assignees', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    """Admin configuration for TaskAttachment model"""
    list_display = ('task', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('task__title', 'uploaded_by__email')
    readonly_fields = ('uploaded_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model"""
    list_display = ('task', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'task__title', 'author__email')
    readonly_fields = ('created_at', 'updated_at')
