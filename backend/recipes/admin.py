from django.contrib import admin

from .models import (FavoriteReceipe, Ingredient, IngredientInRecipesAmount,
                     Recipe, ShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    ordering = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
    )
    list_filter = ('name',)


@admin.register(IngredientInRecipesAmount)
class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('amount', 'ingredient', 'recipe')


class IngredientInRecipesAmountInline(admin.TabularInline):
    model = IngredientInRecipesAmount
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
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
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )
    empty_value_display = '-пусто-'
