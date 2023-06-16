from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        verbose_name='Название',
        help_text='Название тэга',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='HEX-код',
        help_text='HEX-код для обозначения цвета тэга',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Имя для URL',
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        verbose_name='Ингредиент',
        help_text='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        help_text='Единица измерения количества ингредиента',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для рецептов."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Тэги по рецепту',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор публикации рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Ингредиенты для приготовления по рецепту',
        through='IngredientInRecipesAmount',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200)
    image = models.ImageField(
        'Фотография блюда',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления блюда',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientInRecipesAmount(models.Model):
    """
    Вспомогательная модель для просмотра количества
    ингредиентов в рецепте.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
    )

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Необходимое количество данного ингредиента',
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient',
            )
        ]


class FavoriteReceipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Рецепты в избранном'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_recipe',
            )
        ]


class ShoppingCart(models.Model):
    """Модель для списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipes',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe_in_shopping_cart',
            )
        ]
