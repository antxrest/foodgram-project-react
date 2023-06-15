from django.contrib import admin

from recipes.models import (Favorite, Ingredient, RecipeIngredient, Recipes,
                            ShoppingCart, Tags)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    fields = ['tags', 'name', 'cooking_time', 'author', 'image', 'text']
    list_display = ('name', 'author', 'favorite_count',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_count',)
    inlines = [RecipeIngredientInline]

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_editable = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('color',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('pk', 'user', 'recipe')
    list_filter  = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('pk', 'user', 'recipe')
    list_filter  = ('user', 'recipe')
    empty_value_display = '-пусто-'
