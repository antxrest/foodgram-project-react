from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Tags(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        verbose_name="Название тега",
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет HEX",
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                "^#([a-fA-F0-9]{6})",
                message="Поле должно содержать HEX-код цвета.",
            )
        ],
    )
    slug = models.SlugField(
        verbose_name="Уникальный слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("id",)

    def __str__(self):
        return f"{self.name}"


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        verbose_name="Название ингредиента", max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения", max_length=200
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}."


class Recipes(models.Model):
    """Модель для рецептов."""

    ingredients = models.ManyToManyField(
        Ingredients,
        through="IngredientsInRecipe",
        verbose_name="Список ингредиентов",
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name="Список тегов",
        related_name="recipes",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        blank=True,
        null=True,
        upload_to="image_recipes/",
    )
    name = models.CharField(verbose_name="Название рецепта", max_length=200)
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (в минутах)",
        validators=[MinValueValidator(1, "Время должно быть от 1 минуты.")],
    )
    pud_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pud_date",)

    def __str__(self):
        return f"{self.name}"


class IngredientsInRecipe(models.Model):
    """Вспомогательная модель для количества ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="ingredients_amount",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name="ingredients_amount",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество в рецепте",
        validators=[
            MinValueValidator(1, "В рецепте должны быть ингредиенты.")
        ],
    )

    class Meta:
        verbose_name = "Ингредиент для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient"), name="unique_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.ingredient.name} - {self.amount}"


class FavouriteRecipes(models.Model):
    """Модель для любимых рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favourites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="favourites",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_user_recipe"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.recipe.name}"


class ShoppingLists(models.Model):
    """Модель для списков покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="list",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="list",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_list_user"
            )
        ]
