"""Кастомные представления приложения 'users'."""
from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Кастомное представление для листинга, создания и удаления записей."""

    pass
