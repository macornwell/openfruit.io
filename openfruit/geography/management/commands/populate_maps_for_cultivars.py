from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django_geo_db.models import Location, LocationMap
from django_geo_db.services import LocationMapGenerator, GEO_DAL
from openfruit.taxonomy.models import Cultivar


class Command(BaseCommand):
    help = "Pre-Populates all maps for every cultivar, if possible. MUST HAVE Site set correctly."

    def handle(self, *args, **options):
        map_type = GEO_DAL.get_map_type('simple')
        for c in Cultivar.objects.all():
            location = c.origin_location
            if location:
                if not LocationMap.objects.filter(location=location).exists():
                    print('Creating Map for {0}-{1}'.format(c, location))
                    try:
                        if location.name:
                            LocationMapGenerator(domain).get_location_map_by_location_name(map_type, location)
                        else:
                            LocationMapGenerator(domain).get_or_generate_location_map(map_type, location)
                        print('Success')
                    except Exception as e:
                        if 'look like a module path' in str(e):
                            raise e
                        print('Failed: {0}'.format(e))

