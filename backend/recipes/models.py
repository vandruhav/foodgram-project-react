"""Модели приложения 'recipes'."""
from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой HEX-код',
        validators=[
            RegexValidator(
                regex='^#[A-Fa-f0-9]{6}$',
                message=('Ошибка формата ввода (формат: #XXXXXX или #xxxxxx,'
                         ' где X или x - шестнадцатеричные цифры в верхнем '
                         'или в нижнем регистрах)!'),
            ),
        ],
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Адрес тега',
    )

    class Meta:
        """Meta-класс модели тегов."""

        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def clean(self):
        """Функция валидации тегов."""
        super().clean()
        self.color = self.color.upper()

    def __str__(self):
        """Функция строкового представления тегов."""
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    class Meta:
        """Meta-класс модели ингредиентов."""

        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=('name', 'measurement_unit',),
                                    name='unique_ingredients',),
        ]

    def __str__(self):
        """Функция строкового представления ингредиентов."""
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты в рецепте',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagInRecipe',
        verbose_name='Теги рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, message='Минимальное время - 1 минута!'),
            MaxValueValidator(
                settings.MAX_SMALL_INT,
                message=f'Максимальное время - {settings.MAX_SMALL_INT} минут!'
            ),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта',
    )

    class Meta:
        """Meta-класс модели рецептов."""

        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        """Функция строкового представления рецептов."""
        return self.name


class IngredientInRecipe(models.Model):
    """Модель ингредиентов в рецептах."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_of_recipe',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipes_of_ingredient',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(1, message='Минимальное количество - 1!'),
            MaxValueValidator(
                settings.MAX_SMALL_INT,
                message=f'Максимальное количество - {settings.MAX_SMALL_INT}!'
            ),
        ],
    )

    class Meta:
        """Meta-класс модели ингредиентов в рецептах."""

        ordering = ('id',)
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient',),
                                    name='unique_recipe_ingredient',),
        ]

    def __str__(self):
        """Строковое представление ингредиентов в рецептах."""
        return f'В {self.recipe} {self.amount} {self.ingredient}'


class TagInRecipe(models.Model):
    """Модель тегов в рецептах."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_of_recipe',
        verbose_name='Рецепт',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes_of_tag',
        verbose_name='Тег',
    )

    class Meta:
        """Meta-класс модели тегов в рецептах."""

        ordering = ('id',)
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'tag',),
                                    name='unique_recipe_tag',),
        ]

    def __str__(self):
        """Строковое представление тегов в рецептах."""
        return f'{self.recipe} на {self.tag}'


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        """Meta-класс модели избранного."""

        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique_favorite_user_recipe',),
        ]

    def __str__(self):
        """Строковое представление избранного."""
        return f'{self.user} избрал {self.recipe}'


class Cart(models.Model):
    """Модель корзины."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        """Meta-класс модели корзины."""

        ordering = ('id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique_cart_user_recipe',),
        ]

    def __str__(self):
        """Строковое представление корзины."""
        return f'{self.user} положил в корзину {self.recipe}'
