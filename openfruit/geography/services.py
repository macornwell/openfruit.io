import os
import csv
from openfruit.settings import BASE_DIR

US_CITIES_FILE = 'us-cities-and-zips.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'


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
    (zip_code,latitude,longitude,city,state)
    :return:
    """
    with open(os.path.join(BASE_DIR, 'openfruit', 'geography', US_CITIES_FILE)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            city = row['city'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            zip = row['zip_code'].strip()
            yield (zip, lat, lon, city, state)


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
