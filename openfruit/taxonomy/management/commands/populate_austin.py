import random
from random import randrange
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.taxonomy.models import Species, Cultivar, FruitingPlant
from openfruit.geography.models import GeoCoordinate, Location, City
from openfruit.geography.utilities import BoundingBox, LatLon

@transaction.atomic
class Command(BaseCommand):
    help = "Populate's austin texas with test objects."

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        print(settings.DEBUG)
        if not settings.DEBUG:
            raise Exception('This is not available in production mode.')
        count = options['count']
        if not str(count).isdigit():
            raise Exception('Need an integer not {0}'.format(count))
        print('Generating {0} plants in Austin.'.format(count))
        count = int(count)
        seedling_count = count // 2
        cultivar_count = count // 2

        north_east = '30.30670 -97.67572'
        south_west = '30.23237 -97.80326'

        admin = User.objects.get(username='admin')
        austin_location = Location.objects.filter(name='Test Austin').first()
        if not austin_location:
            print('Creating "Test Austin" Location')
            city = City.objects.get(generated_name='Austin, Texas')
            austin_location = Location()
            austin_location.city = city
            austin_location.name = 'Test Austin'
            austin_location.save()
        else:
            print('Previous Test Austin exists. Deleting all previous records.')
            FruitingPlant.objects.filter(location__name='Test Austin').delete()

        bb = BoundingBox(LatLon.parse_string(north_east), LatLon.parse_string(south_west))
        species_choices = list(Species.objects.all())
        print('Generating Seedlings')
        for i in range(0, seedling_count):
            latLon = bb.random_coordinate_in_bounding_box()
            species = random.choice(species_choices)
            fruiting_plant = FruitingPlant()
            fruiting_plant.created_by = admin
            fruiting_plant.location = austin_location
            geo, created = GeoCoordinate.objects.get_or_create(lat=latLon.lat, lon=latLon.lon)
            fruiting_plant.geocoordinate = geo
            fruiting_plant.species = species
            fruiting_plant.date_planted = self.get_random_date()
            fruiting_plant.save()

        cultivar_choices = list(Cultivar.objects.all())
        print('Generating Cultivars')
        for i in range(0, cultivar_count):
            latLon = bb.random_coordinate_in_bounding_box()
            cultivar = random.choice(cultivar_choices)
            fruiting_plant = FruitingPlant()
            fruiting_plant.created_by = admin
            fruiting_plant.location = austin_location
            geo, created = GeoCoordinate.objects.get_or_create(lat=latLon.lat, lon=latLon.lon)
            fruiting_plant.geocoordinate = geo
            fruiting_plant.cultivar = cultivar
            fruiting_plant.date_planted = self.get_random_date()
            fruiting_plant.save()

    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def get_random_date(self):
        now = datetime.now()
        start = datetime(2008, 1, 1, 1, 1, 1, 1)
        return self.random_date(start, now)
