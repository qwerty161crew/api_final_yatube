from rest_framework import permissions


class AuthorCreateorDeleteOnly(permissions.BasePermission):
    """удалять пост может только автор"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class GetNotAuchOnly(permissions.BasePermission):
    """гет запрос разрешен неавторизованному пользователю"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return obj.author == request.user
        return False
