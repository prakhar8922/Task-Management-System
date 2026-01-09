from rest_framework import permissions


class IsTaskProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow project members to access tasks.
    """

    def has_object_permission(self, request, view, obj):
        project = obj.project
        return project.owner == request.user or request.user in project.members.all()

    def has_permission(self, request, view):
        """
        Check permission for list/create actions by checking query params
        """
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            # For list/create, we'll check in the view's get_queryset/perform_create
            return request.user.is_authenticated
        return True


class IsCommentAuthor(permissions.BasePermission):
    """
    Custom permission to only allow comment authors to edit/delete their comments.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to project members
        if request.method in permissions.SAFE_METHODS:
            project = obj.task.project
            return project.owner == request.user or request.user in project.members.all()
        
        # Write permissions are only allowed to the comment author
        return obj.author == request.user

    def has_permission(self, request, view):
        """
        Check permission for list/create actions
        """
        return request.user.is_authenticated


class IsAttachmentTaskProjectMember(permissions.BasePermission):
    """
    Custom permission for task attachments - checks task's project membership
    """

    def has_object_permission(self, request, view, obj):
        project = obj.task.project
        return project.owner == request.user or request.user in project.members.all()

    def has_permission(self, request, view):
        """
        Check permission for list/create actions
        """
        return request.user.is_authenticated
