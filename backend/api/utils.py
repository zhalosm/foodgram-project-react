from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import FavoriteSerializer
from recipes.models import Recipe


def add_to(self, model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response({'error': 'Уже существует'},
                        status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, pk=pk)
    instance = model.objects.create(user=user, recipe=recipe)
    serializer = FavoriteSerializer(instance)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def delete_from(self, model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        model.objects.filter(
            user=user, recipe__id=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
