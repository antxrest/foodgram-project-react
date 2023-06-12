from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from users.validators import UserNameValidator, check_username

regex_validator = UserNameValidator()


class User(AbstractUser):
    """Пользовательская модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(max_length=settings.MAX_LENGTH_EMAIL,
                              unique=True,
                              verbose_name='Электронная почта',
                              help_text='Введите e-mail')
    first_name = models.CharField(max_length=settings.MAX_LENGTH_USER,
                                  verbose_name='Имя',
                                  help_text='Введите имя',
                                  validators=[regex_validator])
    last_name = models.CharField(max_length=settings.MAX_LENGTH_USER,
                                 verbose_name='Фамилия',
                                 help_text='Введите фамилию',
                                 validators=[regex_validator])
    password = models.CharField(max_length=settings.MAX_LENGTH_USER,
                                verbose_name='Пароль',
                                help_text='Придумайте пароль')
    username = models.CharField(
        max_length=settings.MAX_LENGTH_USER, unique=True,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя',
        validators=[check_username,
                    UnicodeUsernameValidator()
                    ]
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Подписка на автора рецептурной модели."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='Ограничение повторной подписки'
            ),
            CheckConstraint(
                name="Ограничение на самоподписку",
                check=~models.Q(user=models.F('author')),
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
