"""Маршрутизатор приложения 'users'."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users/subscriptions', FollowViewSet, basename='follow')
router.register(r'users/(?P<id>\d+)/subscribe', FollowViewSet,
                basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
