"""Пользовательские фильтры приложения 'recipes'."""
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter
from users.models import MyUser

from .models import Recipe, Tag


class IngredientFilter(SearchFilter):
    """Поисковый фильтр по названию ингредиентов."""

    search_param = 'name'


class RecipeFilter(FilterSet):
    """Фильтр по тегам, авторам, нахождению в избранном и в корзине."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelChoiceFilter(queryset=MyUser.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        """Функция нахождения данных в избранном."""
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Функция нахождения данных в корзине."""
        if self.request.user.is_authenticated and value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        """Meta-класс фильтра."""

        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)
