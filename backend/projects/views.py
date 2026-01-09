from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Project
from .serializers import ProjectSerializer, ProjectListSerializer
from .permissions import IsProjectOwnerOrMember


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing projects.
    
    list: Get list of projects (owned or member)
    retrieve: Get project details
    create: Create a new project
    update: Update project (owner only)
    partial_update: Partially update project (owner only)
    destroy: Delete project (owner only)
    add_member: Add a member to the project (owner only)
    remove_member: Remove a member from the project (owner only)
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsProjectOwnerOrMember]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        """
        Return projects where user is owner or member
        """
        user = self.request.user
        return Project.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Set the owner to the current user when creating a project
        """
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        """
        Add a member to the project (owner only)
        """
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can add members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            project.members.add(user)
            return Response({'message': f'{user.email} added to project'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        """
        Remove a member from the project (owner only)
        """
        project = self.get_object()
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can remove members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            if user == project.owner:
                return Response(
                    {'error': 'Cannot remove project owner'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            project.members.remove(user)
            return Response({'message': f'{user.email} removed from project'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
