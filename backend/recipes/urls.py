"""Маршрутизатор приложения 'recipes'."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='Tag')
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('recipes', RecipeViewSet, basename='Recipe')

urlpatterns = [
    path('', include(router.urls)),
]
