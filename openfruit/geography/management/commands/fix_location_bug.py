import csv
from django.core.management.base import BaseCommand
from django_geo_db.models import Location
from openfruit.taxonomy.models import Cultivar

def print_2(location, content):
    if location.generated_name is None:
        raise Exception('None for: ' + str(location))
    print('{0}: {1}'.format(location.generated_name, content))

class Command(BaseCommand):
    help = "Removes duplicate locations, intelligently, with lots of memory usage."


    def handle(self, *args, **options):
        location_to_id = {}
        # Iterate through every location that has a city but no zipcode
        for location in Location.objects.all():
            value = location.generated_name
            # If we haven't seen this location before cache it.
            if value not in location_to_id:
                location_to_id[value] = location.location_id
            id = location_to_id[value]

            # If this location's is greater than a previous one, then we need to
            # delete this one AFTER moving all cultivars to the lower value one.
            # the
            if location.location_id > id:
                for c in Cultivar.objects.filter(origin_location=location.location_id):
                    print_2(location, 'Changing location for: ' + c.name)
                    c.origin_location_id = id
                    #c.save()
                print_2(location, 'Deleting New location:' + str(location.location_id))
                print_2(location, 'New location:' + str(location))
                print_2(location, 'Old location:' + str(Location.objects.get(pk=id)))
                #location.delete()
            # If this location is lower than the old one, then that means this one
            # should be kept while the old one is deleted.
            elif location.location_id < id:
                for c in Cultivar.objects.filter(origin_location=id):
                    print_2(location, 'Changing location for: ' + c.name)
                    c.origin_location_id = location.location_id
                    #c.save()
                old_location = Location.objects.get(pk=id)
                print_2(location, 'Deleting Old Location:' + str(old_location.location_id))
                print_2(location, 'New location:' + str(location))
                print_2(location, 'Old location:' + str(Location.objects.get(pk=id)))
                #old_location.delete()
            else:
                # This situation is when they are the same. This will only happen once.
                pass
