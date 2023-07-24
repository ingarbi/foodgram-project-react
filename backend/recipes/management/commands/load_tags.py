import json

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Импортируй  JSON data в модель Tag'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            with open(file_path) as file:
                data = json.load(file)
                for item in data:
                    Tag.objects.create(
                        name=item['name'],
                        color=item['color'],
                        slug=item['slug']
                    )
            if Tag.objects.count() > 0:
                self.stdout.write(
                    self.style.SUCCESS('Data loaded successfully.')
                )
            else:
                self.stdout.write(self.style.ERROR('No data loaded.'))
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('File not found. \
                                Please provide a valid file path.'))
