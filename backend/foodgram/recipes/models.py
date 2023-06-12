from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_slug
from django.db import models

from recipes.validators import ColorValidator
from users.validators import UserNameValidator

User = get_user_model()


regex_validator = UserNameValidator()


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=settings.MAX_LENGTH_INGREDIENT,
                            verbose_name='Название инградиента',
                            help_text='Введите название ингредиента',
                            validators=[regex_validator])
    measurement_unit = models.CharField(
        max_length=settings.MAX_LENGTH_MEAS_UNIT,
        verbose_name='Единица измерения',
        help_text='Введите единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredients',
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tags(models.Model):
    """Модель тега."""
    name = models.CharField(max_length=settings.MAX_LENGTH_TAGS,
                            unique=True,
                            verbose_name='Название тега',
                            help_text='Введите название тега',
                            validators=[regex_validator])
    color = models.CharField(
        max_length=settings.MAX_LENGTH_TAGS_COLOR,
        unique=True,
        verbose_name='Цвет в HEX',
        help_text='Введите цвет тега в виде HEX-кода',
        validators=[ColorValidator]
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_TAGS_SLUG,
        unique=True,
        verbose_name='Слаг',
        help_text='Введите короткое название тега',
        validators=[validate_slug]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug


class Recipes(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Пользователь, написавший рецепт',
        related_name='recipe'
    )
    name = models.CharField(
        max_length=settings.MAX_LENGTH_RECIPES,
        unique=True,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        validators=[regex_validator]
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/image/',
        help_text='Добавьте файл с изображением'
    )
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tags, verbose_name='Теги')
    pub_date = models.DateTimeField(auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1, message=(
                    'Время приготовления не может быть меньше 1 минуты!'
                )
            )
        ],
        default=1,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    """Модель количества ингредиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Рецепт',
        help_text='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество инградиентов',
        help_text='Введите количество инградиента в рецепте',
        default=1,
        validators=[
            MinValueValidator(1, message='Минимальное количество - 1')
        ]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='Уникальный ингридиент в рецепте'),
        )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(models.Model):
    """Модель избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Избранный рецепт',
        help_text='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorites',
            ),
        )


class ShoppingCart(models.Model):
    """Модель корзины для покупок."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Рецепт в списке покупок',
        help_text='Рецепт в списке покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
