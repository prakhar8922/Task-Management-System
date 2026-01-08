from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    owner_detail = UserSerializer(source='owner', read_only=True)
    members_detail = UserSerializer(source='members', many=True, read_only=True)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'owner', 'owner_detail',
            'members', 'members_detail', 'task_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for project lists"""
    owner_detail = UserSerializer(source='owner', read_only=True)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'owner_detail', 'task_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
