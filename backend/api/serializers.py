import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from recipes.models import (Ingredient,
                            RecipeIngredient,
                            Recipes,
                            Favorite,
                            Tags)
from users.models import User, Follow


class Base64ImageField(serializers.ImageField):
    """Сериализатор для картинка в base64."""

    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, author, *args, **kwargs):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return request.user.from_follower.filter(author=author).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredients."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    class Meta:
        model = Favorite
        fields = ('id',)


class IngredientsToRecipesSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient_id')
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, recipes):
        return recipes.ingredient.measurement_unit

    def get_name(self, recipes):
        return recipes.ingredient.name


class IngredientsToRecipesCreateSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True
    )
    recipes = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='ingredient'
    )
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipes', 'amount')


class RecipesListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(
        read_only=True,
        many=True
    )
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorite',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, recipes, *args, **kwargs):
        return IngredientsToRecipesSerializer(
            recipes.ingredients.all(), many=True).data

    def get_is_favorite(self, recipes, *args, **kwargs):
        data = self.context.get('request')
        if data is None or data.user.is_anonymous:
            return False
        return data.user.Favorite.filter(recipe=recipes.id).exists()

    def get_is_in_shopping_cart(self, recipes, *args, **kwargs):
        data = self.context.get('request')
        if data is None or data.user.is_anonymous:
            return False
        return data.user.shoppingcart.filter(recipe=recipes.id).exists()


class RecipesSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all()
    )
    image = Base64ImageField(required=True,)
    ingredients = IngredientsToRecipesCreateSerializer(
        many=True,
    )

    class Meta:
        model = Recipes
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    @staticmethod
    def save_ingredients(recipes, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['id']
            current_amount = int(ingredient['amount'])
            ingredients_list.append(
                RecipeIngredient(
                    recipes=recipes,
                    ingredient=current_ingredient,
                    amount=current_amount
                )
            )
        RecipeIngredient.objects.bulk_create(ingredients_list)

    def to_representation(self, instance):
        return RecipesListSerializer(instance).data

    def validate(self, data):
        cooking_time = data.get('cooking_time')
        if cooking_time <= 0:
            raise serializers.ValidationError(
                {
                    'Ошибка': 'Время не может быть меньше минуты'
                }
            )
        ingredients_list = []
        ingredients_amount = data.get('ingredients')
        for ingredient in ingredients_amount:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    {
                        'Ошибка': 'Количество не может быть меньше 1'
                    }
                )
            ingredients_list.append(ingredient['id'])
        if len(ingredients_list) > len(set(ingredients_list)):
            raise serializers.ValidationError(
                {
                    'Ошибка': 'Ингридиент должен быть уникальный'
                }
            )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            recipe.ingredients.all().delete()
            self.save_ingredients(recipe, ingredients)
        tags = self.initial_data.pop("tags")
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class FollowRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def validate(self, data):
        user = self.context.get('request').user
        following = data.get('following')
        if Follow.objects.filter(user=user, following=following):
            raise serializers.ValidationError(
                f'Вы уже подписаны на автора {following}!'
            )
        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписыватся на самого себя!'
            )
        return data

    def get_is_subscribed(self, following, *args, **kwargs):
        try:
            status = Follow.objects.filter(
                user=self.context.get(
                    'request').user, author=following).exists()
            return status
        except Exception:
            return False

    def get_recipes(self, obj):
        queryset = (
            obj.author.recipes.all())
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                raise ValueError('Неверно задан параметр количества рецептов')
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()
