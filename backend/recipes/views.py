import django_filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Tag, Ingredient, Recipe, Favorite
from .permissions import AuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipesInFollowSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#    @action(detail=True, methods=['get', 'delete'],
#            permission_classes=[IsAuthenticated])
#    def favorite(self, request, pk=None):
#        if request.method == 'GET':
#            return self.add_obj(Favorite, request.user, pk)
#        elif request.method == 'DELETE':
#            return self.delete_obj(Favorite, request.user, pk)
#        return None

#    def add_obj(self, model, user, pk):
#        if model.objects.filter(user=user, recipe__id=pk).exists():
#            return Response({
#                'errors': 'Рецепт уже добавлен в список'
#            }, status=status.HTTP_400_BAD_REQUEST)
#        recipe = get_object_or_404(Recipe, id=pk)
#        model.objects.create(user=user, recipe=recipe)
#        serializer = RecipesInFollowSerializer(recipe)
#        return Response(serializer.data, status=status.HTTP_201_CREATED)

#    def delete_obj(self, model, user, pk):
#        obj = model.objects.filter(user=user, recipe__id=pk)
#        if obj.exists():
#            obj.delete()
#            return Response(status=status.HTTP_204_NO_CONTENT)
#        return Response({
#            'errors': 'Рецепт уже удален'
#        }, status=status.HTTP_400_BAD_REQUEST)
