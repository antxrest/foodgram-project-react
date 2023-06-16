from django.contrib import admin

from .models import (FavoriteReceipe, Ingredient, IngredientInRecipesAmount,
                     Recipe, ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ панель управления ингредиентами."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ панель управления тегами."""
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipesAmount)
class AmountIngredientAdmin(admin.ModelAdmin):
    """Отображение ингредиентов в админке."""
    list_display = ('amount', 'ingredient', 'recipe')


class IngredientInRecipesAmountInline(admin.TabularInline):
    """Отображение ингредиентов в рецептах в админ панели."""
    model = IngredientInRecipesAmount
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ панель управления рецептами."""
    list_display = ('name', 'author', 'get_in_favorites')
    list_filter = (
        'name',
        'author',
        'tags',
    )
    inlines = (IngredientInRecipesAmountInline,)
    empty_value_display = '-пусто-'

    def get_in_favorites(self, obj):
        return obj.favorite_recipes.count()


@admin.register(FavoriteReceipe)
class FavoriteReceipeAdmin(admin.ModelAdmin):
    """Админ панель управления подписками."""
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ панель списка покупок."""
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    search_fields = ('user', )
    empty_value_display = '-пусто-'
