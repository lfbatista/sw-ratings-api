from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit their objects."""

    def has_object_permission(self, request, view, obj):
        """Read (GET, HEAD, OPTIONS) permissions are allowed to any request."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
