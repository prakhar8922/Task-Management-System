from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Task, Tag, TaskAttachment, Comment
from .serializers import (
    TaskSerializer, TaskListSerializer, TaskDetailSerializer,
    TagSerializer, TaskAttachmentSerializer, CommentSerializer
)
from .permissions import IsTaskProjectMember, IsCommentAuthor, IsAttachmentTaskProjectMember
from projects.permissions import IsProjectMember


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    
    list: Get list of tasks (filtered by project if provided)
    retrieve: Get task details with comments and attachments
    create: Create a new task
    update: Update task
    partial_update: Partially update task
    destroy: Delete task
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsTaskProjectMember]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    def get_queryset(self):
        """
        Return tasks filtered by project and user permissions
        """
        queryset = Task.objects.all()
        project_id = self.request.query_params.get('project', None)
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by assignee if provided
        assignee_id = self.request.query_params.get('assignee', None)
        if assignee_id:
            queryset = queryset.filter(assignees__id=assignee_id)
        
        # Filter by priority if provided
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.distinct()

    def perform_create(self, serializer):
        """
        Set the created_by field to the current user
        """
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        """
        Override get_permissions to check project membership on object level
        """
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsTaskProjectMember]
        return [permission() for permission in permission_classes]


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing task attachments.
    """
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsAuthenticated, IsAttachmentTaskProjectMember]

    def get_queryset(self):
        """
        Return attachments for a specific task
        """
        task_id = self.request.query_params.get('task', None)
        if task_id:
            return TaskAttachment.objects.filter(task_id=task_id)
        return TaskAttachment.objects.none()

    def perform_create(self, serializer):
        """
        Set the uploaded_by field to the current user
        """
        serializer.save(uploaded_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing task comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        """
        Return comments for a specific task
        """
        task_id = self.request.query_params.get('task', None)
        if task_id:
            return Comment.objects.filter(task_id=task_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        """
        Set the author field to the current user
        """
        serializer.save(author=self.request.user)

