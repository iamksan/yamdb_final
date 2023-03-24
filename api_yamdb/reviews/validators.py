from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if current_year < value:
        raise ValidationError(
            'Год выпуска не может быть больше текущего года!'
        )
