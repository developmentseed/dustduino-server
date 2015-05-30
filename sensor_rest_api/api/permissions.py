from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # So we'll always allow GET, HEAD, or OPTIONS request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return (obj.owner == request.user or request.user.is_staff)

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow user to update own object
    """
    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        if view.action in ['retrieve', 'update', 'destroy']:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # So we'll always allow GET, HEAD, or OPTIONS request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return (obj == request.user or request.user.is_staff)
