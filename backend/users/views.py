from http import HTTPStatus
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .custom_viewsets import ListCreateDestroyViewSet
from .models import Follow, MyUser
from .serializers import FollowSerializer


class FollowViewSet(ListCreateDestroyViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        author = get_object_or_404(MyUser, id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, author=author)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(MyUser, id=self.kwargs.get('id'))
        get_object_or_404(Follow, user=self.request.user,
                          author=author).delete()
        return Response(status=HTTPStatus.NO_CONTENT)
