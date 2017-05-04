import os
import csv
from openfruit.settings import BASE_DIR
from openfruit.geography.models import UserGeographySettings, UserLocation

US_CITIES_FILE = 'us-cities-and-zips.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'

class GeographyDAL:

    def get_users_locations(self, user):
        return UserLocation.objects.filter(user=user).values_list('location', flat=True)

    def get_users_geography_settings(self, user):
        return UserGeographySettings.objects.filter(user=user).first()

    def append_user_location(self, user, locationUsedByUser):
        obj, created = UserLocation.objects.get_or_create(user=user, location=locationUsedByUser)
        if not created:
            obj.save()  # This triggers the updating of the date.

GEO_DAL = GeographyDAL()


def generate_current_us_states_list():
    """
    Iterates through a list of all of the US States.
    (state, abbreviation, latitude, longitude)
    :return:
    """
    with open(os.path.join(BASE_DIR, 'openfruit', 'geography', US_STATES_FILE)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            abbreviation = row['abbreviation'].strip()
            latitude = row['latitude'].strip()
            longitude = row['longitude'].strip()
            yield (state, abbreviation, latitude, longitude)


def generate_current_us_cities_list():
    """
    Iterates through a list of all of the US cities.
    (zip_code,latitude,longitude,city,state, timezone)
    :return:
    """
    with open(os.path.join(BASE_DIR, 'openfruit', 'geography', US_CITIES_FILE)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            city = row['city'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            zip = row['zip'].strip()
            timezone = row['timezone']
            yield (zip, lat, lon, city, state, timezone)


def generate_countries():
    """
    Iterates through a list of all of the US cities.
    (country name, continent,abbreviation,latitude,longitude)
    :return:
    """
    with open(os.path.join(BASE_DIR, 'openfruit', 'geography', COUNTRIES_FILE)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            abbr = row['abbreviation'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            country = row['name'].strip().replace('"', '')
            continent = row['continent'].strip()
            yield (country, continent, abbr, lat, lon)
