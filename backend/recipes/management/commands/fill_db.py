import csv
from django.core.management.base import BaseCommand

from ...models import Ingredient

file_table = {
    'ingredients.csv': Ingredient,
}


class Command(BaseCommand):
    help = 'Заполнение БД'

    def handle(self, *args, **options):
        for file, table in file_table.items():
            with open(f'../data/{file}', 'r', encoding='utf8') as f:
                fieldnames = ['name', 'measurement_unit']
                dr = csv.DictReader(f, delimiter=',', fieldnames=fieldnames)
                for row in dr:
                    if file == 'ingredients.csv':
                        name = row.pop('name')
                        unit = row.pop('measurement_unit')
                        table.objects.get_or_create(name=name,
                                                    measurement_unit=unit)
                self.stdout.write(f'Таблица {table.__name__} заполнена!')
