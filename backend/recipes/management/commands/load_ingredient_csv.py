import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_name = 'recipes/data/ingredients.csv'
        with open(file_name, 'r', encoding='utf-8') as file:
            print(file)
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                try:
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                except IntegrityError:
                    print(f'Ингредиент {name} {measurement_unit}'
                          f' есть в базе')
