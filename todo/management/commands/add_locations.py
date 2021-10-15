from django.core.management import BaseCommand

from todo.models import Locations


class Command(BaseCommand):
    help = "Adds initial locations to the database"

    def create_locations(self):
        cities = ['Istanbul', 'London', 'Oslo', 'Bologna', 'Madrid', 'Malaga', 'Turin', 'Munich', 'Rome', 'Durham',
                  'Bruges', 'Salzburg']
        for city in cities:
            Locations.objects.create(city=city)

    def handle(self, *args, **options):
        print("Adding Locations Now")
        self.create_locations()
