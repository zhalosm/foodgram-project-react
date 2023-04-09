from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [models.UniqueConstraint(
            fields=['username'],
            name='unique_username'
        ),
            models.UniqueConstraint(
            fields=['email'],
            name='unique_email'
        )
        ]

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                'Пользователь не может подписаться на самого себя'
            )

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
