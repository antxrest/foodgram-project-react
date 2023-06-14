import django_filters
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

from recipes.models import Recipes, Tags

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = django_filters.CharFilter(field_name='author')
    tags = django_filters.AllValuesMultipleFilter(method='filter_tags')

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_tags(self, queryset, tags):
        slug_id_list = []
        if tags:
            for tag in tags:
                ([slug_id_list.append(temp_tag.pk)
                    for temp_tag in Tags.objects.filter(slug=tag)])
            queryset = queryset.filter(tags__pk__in=slug_id_list)
            return queryset.filter(tags__pk__in=slug_id_list)
        return queryset

    def filter_is_favorited(self, queryset, value):
        if value and self.request.user.is_authenticated:
            temp_queryset = self.request.user.favorites.values('recipes_id')
            return queryset.filter(id__in=temp_queryset)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        if value and self.request.user.is_authenticated:
            temp_queryset = self.request.user.shopping_cart.values('recipes_id')
            return queryset.filter(id__in=temp_queryset)
        return queryset
