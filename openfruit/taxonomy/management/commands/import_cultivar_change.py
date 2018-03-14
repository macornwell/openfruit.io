import csv
from datetime import date
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django_geo_db.models import Location, State, County, City, Zipcode
from openfruit.taxonomy.models import Cultivar, Species
from django.db import transaction

ZIP_RE = re.compile('\d+')
COORD_RE = re.compile('-?\d{1,2}\.\d{4,6} -?\d{1,3}\.\d{4,6}')

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
        if ',' in location:
            a, b = location.split(',')
            a = a.strip()
            b = b.strip()
            a_is_county = False
            if 'County' in a or 'Parish' in a:
                a = a.replace('County', '')
                a = a.replace('Parish', '')
                a_is_county = True
                coord_match = COORD_RE.search(b)
                lat_lon = None
                if coord_match:
                    lat_lon = coord_match.group(0)
                    b = b.replace(lat_lon, '')
                    b = b.strip()
                zip_match = ZIP_RE.search(b)
                zip_value = None
                if zip_match:
                    zip_value = zip_match.group(0)
                    b = b.replace(zip_value, '')
                    b = b.strip()
                state = b
                location_obj = None

            else:
                pass  # a is city
        else:
            location = location.strip()
            state = State.objects.filter(name=location).first()
            if not state:  # Location is Country
                country = Location.objects.filter(country=location, state=None, name=None).first()
                if not country:
                    raise Exception('Country {0} does not exist.'.format(location))
                else:
                    print('Setting {0} location to {1}'.format(cultivar, country))
                    cultivar.origin_location = country
            else:
                print('Setting {0} location to {1}'.format(cultivar, state))
                cultivar.origin_location = state







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
                    cultivar = Cultivar.objects.get(name__iexact=name)

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
                    #cultivar.save()

                except Exception as e:
                    print(row)
                    raise e

