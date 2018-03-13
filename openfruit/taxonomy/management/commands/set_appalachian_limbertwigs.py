from django.db.models import Q
from django.core.management.base import BaseCommand
from django_geo_db.models import Location
from openfruit.taxonomy.models import Cultivar

class Command(BaseCommand):
    help = "Sets Limbertwigs with no state to an Appalachia location. NOTE: Appalachia must exist."

    def handle(self, *args, **options):
        appalachia = Location.objects.get(state=None, name='Appalachia')
        for c in Cultivar.objects.filter(name__icontains='Limbertwig', origin_location__state=None)\
                .filter(~Q(origin_location=appalachia)):
            c.origin_location = appalachia
            print('Saving {0} to appalchia.'.format(c))
            c.save()

