from django.contrib import admin

from .models import (
    Cart, Favorite, Ingredient, IngredientInRecipe, Recipe, Tag, TagInRecipe
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_editable = ('recipe', 'ingredient',)
    empty_value_display = '-пусто-'


class TagInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag',)
    list_editable = ('recipe', 'tag',)
    empty_value_display = '-пусто-'


class IngredientInRecipeInLine(admin.TabularInline):
    model = IngredientInRecipe
    extra = 0


class TagInRecipeInLine(admin.TabularInline):
    model = TagInRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInLine, TagInRecipeInLine,)
    list_display = ('id', 'name', 'author', 'favorites',)
    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags__name',)
    empty_value_display = '-пусто-'

    def favorites(self, obj):
        return obj.favorites.count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(TagInRecipe, TagInRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
