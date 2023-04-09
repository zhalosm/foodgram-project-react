from django.core.exceptions import ValidationError


def validate_color_code(value):
    if not value.startswith('#') or len(value) != 7:
        raise ValidationError(
            'Значение поля "color_code" должно быть в формате #RRGGBB'
        )
    try:
        int(value[1:], 16)
    except ValueError:
        raise ValidationError(
            'Значение поля "color_code" должно быть в формате #RRGGBB'
        )


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Время приготовления должно быть не менее одной минуты'
        )


def validate_amount(value):
    if value < 1:
        raise ValidationError(
            'Минимум один ингредиент'
        )
