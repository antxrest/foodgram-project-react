from django.core.exceptions import ValidationError
from django_filters.fields import MultipleChoiceField
from django_filters.rest_framework import CharFilter, FilterSet, filters
from django_filters.widgets import BooleanWidget
from recipes.models import Ingredients, Recipes


class TagsMultipleChoiceField(MultipleChoiceField):
    """Класс для фильтрации обьектов Tags."""

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )
        for val in value:
            if val in self.choices and not self.valid_value(val):
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": val},
                )


class TagsFilter(filters.AllValuesMultipleFilter):
    """Класс для фильтрации обьектов Tags."""

    field_class = TagsMultipleChoiceField


class IngredientsSearchFilter(FilterSet):
    """Класс для фильтрации обьектов Ingredients."""

    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredients
        fields = ("name",)


class RecipesFilter(FilterSet):
    """Класс для фильтрации обьектов Recipes."""

    author = filters.AllValuesMultipleFilter(
        field_name="author__id", label="Автор"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        widget=BooleanWidget(), label="В списке покупок."
    )
    is_favorited = filters.BooleanFilter(
        widget=BooleanWidget(), label="В избранном."
    )
    tags = TagsFilter(field_name="tags__slug")

    class Meta:
        model = Recipes
        fields = ("author", "tags", "is_in_shopping_cart", "is_favorited")
