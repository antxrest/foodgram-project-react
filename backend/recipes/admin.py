from django.contrib import admin

from .models import (FavouriteRecipes, Ingredients, IngredientsInRecipe,
                     Recipes, ShoppingLists, Tags)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """В админке: отображение и редактирование тегов."""

    list_display = ("pk", "name", "slug", "color")
    list_editable = ("name", "slug", "color")


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    """В админке: поиск, отображение, редактирование рецептов."""

    list_display = ("pk", "name", "measurement_unit")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """В админке: отобр. и ред. ингредиентов в рецептах."""

    list_display = ("pk", "recipe", "ingredient", "amount")
    list_editable = ("recipe", "ingredient", "amount")


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    """В админке: отобр. и ред., фильтр, поиск рецептов."""

    list_display = ("pk", "name", "author")
    list_editable = ("name",)
    list_filter = ("name", "author", "tags")
    readonly_fields = ("count_favorites",)
    search_fields = ("name", "author")

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(FavouriteRecipes)
class FavouriteRecipesAdmin(admin.ModelAdmin):
    """В админке: поиск, отображение, редактирование избранного."""

    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")
    search_fields = ("name", "recipe")


@admin.register(ShoppingLists)
class ShoppingListAdmin(admin.ModelAdmin):
    """В админке: поиск, отобр., ред. списка покупок."""

    list_display = ("pk", "user", "recipe")
    list_editable = ("user", "recipe")
    search_fields = ("user", "recipe")
