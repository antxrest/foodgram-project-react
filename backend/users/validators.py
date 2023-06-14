from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def check_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "Me, ME, me, mE'
        )


class UserNameValidator(RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z -]+$'
    message = (
        'Введите правильное имя. Оно должно включать только буквы, '
        'пробел и дефис.'
    )
    flags = 0
