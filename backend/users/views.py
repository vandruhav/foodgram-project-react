"""Представления приложения 'users'."""
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .custom_viewsets import ListCreateDestroyViewSet
from .models import Follow, MyUser
from .serializers import FollowSerializer


class FollowViewSet(ListCreateDestroyViewSet):
    """Представление для работы с подписками."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Функция для получения набора данных."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Функция для работы с созданием подписки."""
        author = get_object_or_404(MyUser, id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, author=author)

    def delete(self, request, *args, **kwargs):
        """Функция для работы с удалением подписки."""
        author = get_object_or_404(MyUser, id=self.kwargs.get('id'))
        get_object_or_404(Follow, user=self.request.user,
                          author=author).delete()
        return Response(status=HTTPStatus.NO_CONTENT)
