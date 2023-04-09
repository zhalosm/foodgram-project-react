from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeWriteSerializer, TagSerializer)
from api.utils import add_to, delete_from
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                            Tag)
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from users.permissions import AuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        """Возвращает соответствующий класс сериализатора."""
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Добавляет или удаляет рецепт из избранного."""
        if request.method == 'POST':
            return add_to(self, Favorite, request.user, pk)
        return delete_from(self, Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Добавляет или удаляет рецепт из корзины пользователя."""
        if request.method == 'POST':
            return add_to(self, ShoppingCart, request.user, pk)
        return delete_from(self, ShoppingCart, request.user, pk)


class DownloadCart(APIView):
    """View для скачивания списка покупок"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Скачивает список покупок в формате .txt."""
        shopping_list = {}
        ingredients = Amount.objects.filter(
            recipe__in_shopping_cart__user=request.user
        )
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
        main_list = ([f"* {item}:{value['amount']}"
                      f"{value['measurement_unit']}\n"
                      for item, value in shopping_list.items()])
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
