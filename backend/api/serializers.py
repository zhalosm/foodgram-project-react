from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import Base64ImageField
from recipes.models import Amount, Ingredient, Recipe, Tag
from users.models import Follow
from users.serializers import UsersSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountSerializer(serializers.Serializer):
    """Сериализатор для колиечества ингредиентов."""
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Ингредиентов не может быть ноль.'
            )
        if value > 2147483647:
            raise serializers.ValidationError(
                'Недопустимое количество ингредиентов.'
            )
        return value


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецепта."""
    author = UsersSerializer(read_only=True)
    ingredients = AmountSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        """Проверяет находится ли рецепт в избранном."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Проверяет находится ли рецепт в в списке покупок."""
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.cart.filter(recipe=obj).exists()
        )


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def add_ingredients(self, ingredients_list, recipe):
        """Добавляет несколько ингредиентов."""
        Amount.objects.bulk_create([
            Amount(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            ) for ingredient in ingredients_list
        ])

    def create(self, validated_data):
        """Создает новый рецепт."""
        request = self.context.get('request')
        author = request.user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.add(*tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Обновялет существующий рецепет."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        Amount.objects.filter(recipe_id=instance.pk).delete()
        self.add_ingredients(ingredients, instance)
        super().update(instance, validated_data)
        return instance


class FavoriteSerializer(serializers.Serializer):
    """Сериализатор для избарнных рецептов."""
    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class FollowListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

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
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        """Получение количества рецептов для конкретного автора."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Получение списка авторских рецептов."""
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeShortSerializer(
                Recipe.objects.filter(author=obj),
                many=True,
                context={'request': request}
            ).data
        return RecipeShortSerializer(
            Recipe.objects.filter(author=obj)[:int(recipes_limit)],
            many=True,
            context={'request': request}
        ).data

    def get_is_subscribed(self, obj):
        """Статус подписки текущего пользователя на конкретного автора."""
        request = self.context.get('request')
        user = request.user if request else None
        return (
            user and not user.is_anonymous
            and user.follower.filter(author=obj).exists()
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    class Meta:
        model = Follow
        fields = ('author', 'user')

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.author,
            context={'request': request}
        ).data

    def validate(self, data):
        """Проверяет подписан ли пользователь на автора."""
        request = self.context.get('request')
        user = request.user
        author = data.get('author')
        if Follow.objects.filter(user=user, author=author):
            raise serializers.ValidationError('Вы уже подписаны')
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя'
            )
        return data
