"""Разрешения приложения 'recipes'."""
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешения для чтения записей любым пользователем и создания,
    изменения и удаления записей автором и суперпользователем."""

    def has_permission(self, request, view):
        """Функция разрешений на уровне запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Функция разрешений на уровне объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or obj.author == request.user
        )
