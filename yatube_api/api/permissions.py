from rest_framework import permissions


class AuthorDeleteOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method in 'DELETE':
                if obj.author == request.user:
                    return True
                return False
            return obj.author == request.user
        return False
