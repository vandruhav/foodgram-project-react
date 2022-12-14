"""Сериализаторы приложения 'recipes'."""
import base64

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import MyUserSerializer

from .models import Ingredient, IngredientInRecipe, Recipe, Tag


class Base64ImageField(serializers.ImageField):
    """Класс поля для хранения фото."""

    def to_internal_value(self, data):
        """Функция декодирования данных."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        """Meta-класс сериализатора тегов."""

        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        """Meta-класс сериализатора ингредиентов."""

        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецептах."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        """Meta-класс сериализатора ингредиентов в рецептах."""

        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(source='ingredients_of_recipe',
                                               many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        """Meta-класс сериализатора рецептов."""

        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        """Функция определения нахождения рецепта в избранном."""
        user = self.context.get('request').user
        return (
                user.is_authenticated
                and Recipe.objects.filter(
                    favorites__user=user, id=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Функция определения нахождения рецепта в корзине."""
        user = self.context.get('request').user
        return (
                user.is_authenticated
                and Recipe.objects.filter(cart__user=user, id=obj.id).exists()
        )

    def validate(self, data):
        """Функция валидации данных."""
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError('Добавьте тег!')
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError('Добавьте ингредиент!')
        total_ingredients = []
        for ingredient in ingredients:
            obj = get_object_or_404(Ingredient, id=ingredient['id'])
            if obj in total_ingredients:
                raise serializers.ValidationError('Ингредиент есть в рецепте!')
            try:
                amount = int(ingredient['amount'])
            except Exception:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть целым числом!'
                )
            if amount < 1 or amount > settings.MAX_SMALL_INT:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть от 1 до '
                    f'{settings.MAX_SMALL_INT}!'
                )
            total_ingredients.append(obj)
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        """Функция создания ингредиентов."""
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        """Функция создания рецепта."""
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Функция обновления рецепта."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientInRecipe.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipesInFollowSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов в подписках."""

    class Meta:
        """Meta-класс сериализатора рецептов в подписках."""

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
