from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from .views import FollowViewSet

app_name = 'users'

# router = DefaultRouter()
# router.register('users/subscriptions', FollowViewSet, basename='follow')

urlpatterns = [
#    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
