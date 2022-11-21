from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import MyUser, Follow


class MyUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = MyUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password',)


class MyUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
                user.is_authenticated
                and Follow.objects.filter(user=user, author=obj).exists()
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
                user.is_authenticated
                and Follow.objects.filter(
                    user=user, author__id=obj.author.id
                ).exists()
        )

    def get_recipes(self, obj):
        from recipes.models import Recipe
        from recipes.serializers import RecipesInFollowSerializer
        try:
            recipes_limit = int(
                self.context.get('request').query_params['recipes_limit']
            )
            recipes = Recipe.objects.filter(author=obj.author)[:recipes_limit]
        except Exception:
            recipes = obj.author.recipes
        return RecipesInFollowSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def validate(self, data):
        user = self.context.get("request").user
        author_id = self.context.get('view').kwargs.get('id')
        author = get_object_or_404(MyUser, id=author_id)
        if user == author:
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена!')
        if Follow.objects.filter(user=user, author=author):
            raise serializers.ValidationError(
                'Подписка уже существует!')
        return data
