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
