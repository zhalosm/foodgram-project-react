import io

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
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


def download_cart(list_ing):
    sans_regular = settings.STATIC_ROOT / 'fonts/OpenSans-Regular.ttf'
    sans_regular_name = 'OpenSans-Regular'
    sans_bold = settings.STATIC_ROOT / 'fonts/OpenSans-Bold.ttf'
    sans_bold_name = 'OpenSans-Bold'

    pdfmetrics.registerFont(TTFont(sans_regular_name, sans_regular))
    pdfmetrics.registerFont(TTFont(sans_bold_name, sans_bold))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont(sans_bold_name, 32)
    c.drawString(30, 775, 'Foodgram')

    c.setFont(sans_regular_name, 20)
    c.drawString(30, 740, 'Ваш продуктовый помошник')
    c.line(30, 730, 580, 730)

    c.drawString(30, 710, 'Список покупок')
    val = 680
    for step, ing in enumerate(list_ing):
        ingredient = list(ing.values())
        product = ingredient[0]
        unit = ingredient[1]
        amount = ingredient[2]
        string = f'{step+1}. {product} {unit} - {amount}'
        c.drawString(30, val, string)
        val -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='list.pdf'
    )
