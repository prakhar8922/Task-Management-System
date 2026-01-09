from rest_framework import permissions


class IsProjectOwnerOrMember(permissions.BasePermission):
    """
    Custom permission to only allow project owners or members to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to owner and members
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user or request.user in obj.members.all()
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow project members to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.members.all()
