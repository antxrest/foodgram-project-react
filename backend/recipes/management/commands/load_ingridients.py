import json

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.json', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден.'))
            return

        ingredients_to_create = []
        for ingredient in data:
            ingredients_to_create.append(
                Ingredient(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )
            )

        try:
            Ingredient.objects.bulk_create(ingredients_to_create)
            self.stdout.write(self.style.SUCCESS(
                'Ингридиенты успешно импортированы.')
            )
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(
                'Ошибка импорта ингридиентов: {}'.format(str(e)))
            )
