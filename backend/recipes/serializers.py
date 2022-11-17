import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Tag, Ingredient, Recipe, IngredientInRecipe
from users.serializers import MyUserSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(source='ingredients_of_recipe',
                                               many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart','name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, obj):
#        user = self.context.get('request').user
#        if user.is_anonymous:
#            return False
#        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
#        user = self.context.get('request').user
#        if user.is_anonymous:
#            return False
#        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()
        return False


class RecipesInFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
