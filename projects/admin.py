from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model"""
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__email', 'owner__username')
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at')
