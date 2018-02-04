import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openfruit.settings")
import django
django.setup()

from django.contrib.auth.models import User
from django_geo_db.models import Location, City, GeoCoordinate, Country
from openfruit.taxonomy.models import Species, Cultivar, Genus
from openfruit.userdata.models import UserProfile

def script_print(message):
    print('insert_debug_data: {0} '.format(message))

def setup_users():
    script_print('Setting up Users')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

def setup_settings():
    script_print('Setting up Geo Settings')
    settings = UserProfile()
    settings.user = User.objects\
        .get(username='admin')
    settings.location = Location.objects.get(generated_name='Covington, LA 70433')
    settings.save()

def setup_named_locations():
    script_print('Setting up Locations')
    location = Location()
    coord = GeoCoordinate()
    coord.lat = 29.94027
    coord.lon = -89.95040
    coord.save()
    location.geocoordinate = coord
    location.country = Country.objects.get(name__istartswith='United States')
    location.name = 'Urban Farm'
    location.save()

    location = Location()
    coord = GeoCoordinate()
    coord.lat = 30.64516
    coord.lon = -90.02736
    coord.save()
    location.geocoordinate = coord
    location.country = Country.objects.get(name__istartswith='United States')
    location.name = 'Chaba Uti'
    location.save()





def setup_species_cultivars():
    script_print('Setting up Cultivars and Species')
    apple = Species.objects.create(genus=Genus.objects.get(name='Apple'), name='Apple', latin_name='Malus domestica')
    rd = Cultivar.objects.create(species=apple,
                                 name='Red Delicious',
                                 origin_location=Location.objects.filter(city__name='Louisiana', zipcode__isnull=False, state__name='Missouri').first(),
                                 origin_year=1920,
                                 origin_exact=True,
                                 color_dominate_hex='#ff0000',
                                 history='Worst Apple ever created.',
    )


def main():
    setup_users()
    setup_settings()
    setup_named_locations()
    setup_species_cultivars()



if __name__ == '__main__':
    main()


