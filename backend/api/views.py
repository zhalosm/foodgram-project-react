from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.serializers import (IngredientSerializer,
                             RecipeSerializer,
                             RecipeWriteSerializer,
                             TagSerializer)
from api.utils import add_to, delete_from, download_cart
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.permissions import AuthorOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None
    http_method_names = ('get',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return add_to(self, Favorite, request.user, pk)
        return delete_from(self, Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return add_to(self, ShoppingCart, request.user, pk)
        return delete_from(self, ShoppingCart, request.user, pk)


class DownloadCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        list_ing = request.user.cart.values(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit'
        ).order_by('recipe__ingredients__ingredient__name').annotate(
            summ_amount=Sum('recipe__ingredients__amount'))
        return download_cart(list_ing)
