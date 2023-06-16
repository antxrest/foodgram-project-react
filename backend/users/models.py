from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False
    )
    username = models.CharField(
        'Юзернейм',
        max_length=150,
        unique=True,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
        null=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
        null=False
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )]
