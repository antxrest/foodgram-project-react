from django.core import validators
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserNameValidator(validators.RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z -]+$'
    message = _(
        "Введите символы на литинице/кирилице"
    )
    flags = 0


def validate_username(value):
    """Валидатор, не допускающий создания пользователя с логином 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать \'me\' в качестве логина'
        )
    return value
