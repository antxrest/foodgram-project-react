from csv import DictReader

from django.core.management.base import BaseCommand
from recipes.models import Ingredients


class Command(BaseCommand):
    help = "Конвертирование из csv файла"

    def handle(self, *args, **kwargs):
        if Ingredients.objects.exists():
            print("Данные уже загружены!")
            return
        try:
            with open("./data/ingredients.csv", "r", encoding="utf-8") as file:
                reader = DictReader(file)
                Ingredients.objects.bulk_create(
                    Ingredients(**data) for data in reader
                )
        except ValueError:
            print("Неопределенное значение.")
        except Exception:
            print("Что-то пошло не так!")
        else:
            print("Данные загружены!")
