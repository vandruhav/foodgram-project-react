"""Модели приложения 'users'."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class MyUser(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        """Meta-класс модели пользователей."""

        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Функция строкового представления пользователей."""
        return self.get_full_name()


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        """Meta-класс модели подписок."""

        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=('user', 'author',),
                                    name='unique_follow',),
            models.CheckConstraint(check=~models.Q(user=models.F('author')),
                                   name='user_not_author',),
        ]

    def clean(self):
        """Функция валидации подписок."""
        super().clean()
        if self.author == self.user:
            raise ValidationError('Подписка на самого себя запрещена!')

    def __str__(self):
        """Функция строкового представления подписок."""
        return f'{self.user} подписан на {self.author}'
