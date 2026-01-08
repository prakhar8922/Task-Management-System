from rest_framework import serializers
from .models import Task, Tag, TaskAttachment, Comment
from users.serializers import UserSerializer
from projects.serializers import ProjectListSerializer


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'created_at')
        read_only_fields = ('id', 'created_at')


class TaskAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for TaskAttachment model"""
    uploaded_by_detail = UserSerializer(source='uploaded_by', read_only=True)
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = ('id', 'file', 'file_name', 'uploaded_by', 'uploaded_by_detail', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_by_detail', 'uploaded_at')

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author_detail = UserSerializer(source='author', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'task', 'author', 'author_detail', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'author_detail', 'created_at', 'updated_at')


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with nested relationships"""
    assignees_detail = UserSerializer(source='assignees', many=True, read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    project_detail = ProjectListSerializer(source='project', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    attachments_count = serializers.IntegerField(source='attachments.count', read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'project', 'project_detail',
            'status', 'priority', 'due_date', 'assignees', 'assignees_detail',
            'tags', 'tags_detail', 'created_by', 'created_by_detail',
            'comments_count', 'attachments_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task lists"""
    assignees_detail = UserSerializer(source='assignees', many=True, read_only=True)
    tags_detail = TagSerializer(source='tags', many=True, read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'project', 'project_title',
            'status', 'priority', 'due_date', 'assignees_detail',
            'tags_detail', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class TaskDetailSerializer(TaskSerializer):
    """Detailed serializer for task with comments and attachments"""
    comments = CommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('comments', 'attachments')
