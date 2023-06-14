from django.contrib import admin

from recipes.models import (Favorite, Ingredient, RecipeIngredient, Recipes,
                            ShoppingCart, Tags)


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)
    inlines = [RecipeIngredientInline]

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
