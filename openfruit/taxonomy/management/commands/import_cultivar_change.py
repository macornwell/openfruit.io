import csv
from datetime import date
import re

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from django_geo_db.models import Location, State, County, City, Zipcode, Country
from django_geo_db.services import GEO_DAL
from openfruit.taxonomy.models import Cultivar, Species


CITY_RE = re.compile(r"(?P<city>[a-zA-Z0-9\s]+), (?P<state>[a-zA-Z\s]+)$")
COUNTY_RE = re.compile(r"(?P<county>[a-zA-Z0-9\s]+) (County|Parish), (?P<state>[a-zA-Z\s]+)$")
ZIP_CITY_RE = re.compile(r"(?P<city>[a-zA-Z0-9\s]+), (?P<state>[a-zA-Z\s]+) (?P<zip>\d{5})$")
ZIP_COUNTY_RE = re.compile(r"(?P<county>[a-zA-Z0-9\s]+) (County|Parish), (?P<state>[a-zA-Z\s]+) (?P<zip>\d{5})$")
FULL_RE = re.compile(r'(?P<city>[a-zA-Z0-9\s]+), (?P<state>[a-zA-Z\s]+) (?P<zip>\d{5}) (?P<lat>-?\d{1,2}\.\d{4,6}) (?P<lon>-?\d{1,3}\.\d{4,6}) (?P<location_name>.+)$')

@transaction.atomic
class Command(BaseCommand):
    help = "Imports a csv sheet that that changes cultivar entries."

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def _set_if_not_null(self, cultivar, key, value):
        if value:
            print('Setting {0}'.format(key))
            setattr(cultivar, key, value)

    def __parse_location(self, cultivar, location):
        if not location:
            return
        if 'Region' in location:
            raise Exception('Regions cannot be handled yet.')
        us = Country.objects.get(name='United States of America')
        if ',' in location:

            match = FULL_RE.search(location)
            city = None
            county = None
            state = None
            zipcode = None
            lon = None
            lat = None
            location_name = None
            if match:
                city = match.group('city')
                state = match.group('state')
                zipcode = int(match.group('zip'))
                lat = float(match.group('lat'))
                lon = float(match.group('lon'))
                location_name = match.group('location_name')
            else:
                match = ZIP_COUNTY_RE.search(location)
                if match:
                    county = match.group('county')
                    state = match.group('state')
                    zipcode = int(match.group('zip'))
                else:
                    match = ZIP_CITY_RE.search(location)
                    if match:
                        city = match.group('city')
                        state = match.group('state')
                        zipcode = int(match.group('zip'))
                    else:
                        match = COUNTY_RE.search(location)
                        if match:
                            county = match.group('county')
                            state = match.group('state')
                        else:
                            match = CITY_RE.search(location)
                            if match:
                                city = match.group('city')
                                state = match.group('state')
                            else:
                                raise Exception('Location {0} could not be parsed.'.format(location))
            state = State.objects.get(name__iexact=state.strip())
            location_obj = None
            query = Location.objects.filter(country=us)
            if zipcode:
                zipcode = Zipcode.objects.get(zipcode=zipcode)
            if location_name:
                query = query.filter(name=location_name.strip()).first()
                if not query:
                    location_obj = Location()
                    location_obj.country = us
                    location_obj.state = state
                    location_obj.city = City.objects.get(state=state, name__iexact=city)
                    location_obj.zipcode = zipcode
                    location_obj.name = location_name
                    location_obj.geocoordinate = GEO_DAL.get_or_create_geocoordinate(lat, lon)
                    print('Creating {0}'.format(location_obj))
                    location_obj.save()
            else:
                query = query.filter(state=state, zipcode=zipcode)
                if city:
                    query = query.filter(city__name__iexact=city.strip())
                if county:
                    query = query.filter(county__name__iexact=county.strip(), city__isnull=True)
                """
                query = query.filter(state=state)
                """
                location_obj = query.first()
                if not location_obj:
                    print('Location:' + str(location))
                    raise Exception('A location object was expected, but none was found for {0}'.format(location))
            if location_obj:
                print('Setting {0} location to {1}'.format(cultivar, location_obj))
                cultivar.origin_location = location_obj
        else:
            location = location.strip()
            state = State.objects.filter(name=location).first()
            if not state:  # Location is Country
                country = Location.objects.filter(country__name=location, region=None, state=None, name=None).first()
                if not country:
                    raise Exception('Country {0} does not exist.'.format(location))
                else:
                    print('Setting {0} location to {1}'.format(cultivar, country))
                    cultivar.origin_location = country
            else:
                location = Location.objects.get(country=us, state=state, county=None, city=None, zipcode=None)
                print('Setting {0} location to {1}'.format(cultivar, location))
                cultivar.origin_location = location

    def handle(self, *args, **options):

        with open(options['csv_file_path']) as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                try:
                    species = row[0]
                    species = Species.objects.get(latin_name__iexact=species)
                    name = row[1]
                    cultivar = Cultivar.objects.get(species=species, name__iexact=name)

                    origin_location = row[2]
                    self.__parse_location(cultivar, origin_location)

                    origin_year = row[3]
                    self._set_if_not_null(cultivar, 'origin_year', origin_year)

                    origin_exact = row[4]
                    self._set_if_not_null(cultivar, 'origin_exact', origin_exact)

                    color_dominate_hex = row[5]
                    self._set_if_not_null(cultivar, 'color_dominate_hex', color_dominate_hex)

                    color_secondary_hex = row[6]
                    self._set_if_not_null(cultivar, 'color_secondary_hex', color_secondary_hex)

                    color_tertiary_hex = row[7]
                    self._set_if_not_null(cultivar, 'color_tertiary_hex', color_tertiary_hex)

                    ripens_early_mod = row[8]
                    self._set_if_not_null(cultivar, 'ripens_early_mod', ripens_early_mod)

                    ripens_early = row[9]
                    self._set_if_not_null(cultivar, 'ripens_early', ripens_early)

                    ripens_late_mod = row[10]
                    self._set_if_not_null(cultivar, 'ripens_late_mod', ripens_late_mod)

                    ripens_late = row[11]
                    self._set_if_not_null(cultivar, 'ripens_late', ripens_late)

                    chromosome_count = row[12]
                    self._set_if_not_null(cultivar, 'chromosome_count', chromosome_count)

                    parent_a = row[13]
                    if parent_a:
                        parent_a = Cultivar.objects.get(name__iexact=parent_a)
                        cultivar.parent_a = parent_a

                    parent_b = row[14]
                    if parent_b:
                        parent_b = Cultivar.objects.get(name__iexact=parent_b)
                        cultivar.parent_b = parent_b

                    brief_description = row[15]
                    self._set_if_not_null(cultivar, 'brief_description', brief_description)

                    history = row[16]
                    self._set_if_not_null(cultivar, 'history', history)

                    print('Saving {0}'.format(cultivar))
                    cultivar.save()

                except Exception as e:
                    print('Error')
                    print(row)
                    raise e

