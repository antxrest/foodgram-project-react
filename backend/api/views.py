from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.paginators import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoriteSerializer, FollowSerializer,
                             IngredientSerializer, RecipeListSerializer,
                             RecipesWriteSerializer, TagsSerializer)
from recipes.models import Favorite, Ingredient, Recipes, ShoppingCart, Tags

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Работа с рецептами(создание и редактирование), добавление рецептов
    в избранное, добавление в корзину и скачивание списка покупок
    """

    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    filterset_fields = ('tags',)
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'favorite' or self.action == 'shopping_cart':
            return FavoriteSerializer
        return RecipesWriteSerializer

    def get_queryset(self):
        queryset = Recipes.objects.all()
        tags = self.request.query_params.getlist('tags')
        value_shopping_cart = self.request.GET.get('is_in_shopping_cart')
        value_is_favorited = self.request.GET.get('is_favorited')
        if value_is_favorited:
            queryset = (
                RecipeFilter.filter_is_favorited(
                    self, queryset, value_is_favorited))
        if value_shopping_cart:
            queryset = (
                RecipeFilter.filter_is_in_shopping_cart(
                    self, queryset, value_shopping_cart))
        if tags:
            queryset = RecipeFilter.filter_tags(self, queryset, tags)
        return self.filter_queryset(queryset).distinct()

    def add_in_list(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': f'Рецепт уже добавлен в {model.__name__}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipes, pk=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeListSerializer(recipe)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def delete_in_list(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Рецепт не добавлен в {model.__name__}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_in_list(Favorite, request.user, pk)
        return self.delete_in_list(Favorite, request.user, pk)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_in_list(ShoppingCart, request.user, pk)
        return self.delete_in_list(ShoppingCart, request.user, pk)

    @action(methods=['GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = request.user.shopping_cart.values(
            'recipe__ingredients_amount__ingredient__name',
            'recipe__ingredients_amount__ingredient__measurement_unit'
        ).annotate(amount=Sum('recipe__ingredients_amount__amount'))
        shopping_list = 'Список покупок: \n'
        count_ingredients = 0
        for ingr in ingredients:
            count_ingredients += 1
            shopping_list += (
                f'{count_ingredients}) '
                f'{ingr["recipe__ingredients_amount__ingredient__name"]} - '
                f'{ingr["amount"]} '
                f'({ingr["recipe__ingredients_amount__ingredient__measurement_unit"]}) \n'
            )
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            f'attachment; '
            f'filename="{self.request.user.username} shopping list.txt"'
        )
        return response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с тегами"""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вывод ингредиентов """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)
    pagination_class = None


class FollowUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            return Response(
                {"errors": "Вы уже подписаны на автора"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FollowSerializer(
            request.user.follower.create(author=author),
            context={"request": request},
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.user.follower.filter(author=author).exists():
            request.user.follower.filter(
                author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Автор отсутсвует в списке подписок"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SubscriptionsView(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.follower.all()
