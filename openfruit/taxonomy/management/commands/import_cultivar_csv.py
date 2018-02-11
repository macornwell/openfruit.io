import csv
import re
from django.core.management.base import BaseCommand
from django_geo_db import models as GeoModels
from openfruit.taxonomy.models import Cultivar, Species, Genus, Kingdom, FruitUsageType, RIPENING_MONTH_CHOICES


YEAR_RE = re.compile('\d{4}')
USES = {}

def setup_uses():
    data = {
        'b': 'Baking',
        'c': 'Cooking',
        'y': 'Cider',
        'd': 'Drying',
        'f': 'Fresh Eating',
        'j': 'Juice',
        'p': 'Preserves',
        's': 'Storage',
    }
    for c in data:
        value = data[c]
        USES[c] = FruitUsageType.objects.get(type=value)
setup_uses()

RIPENING_MONTH_CHOICES_BACKWARDS = {}

def setup_backwards_ripening():
    for a, b in RIPENING_MONTH_CHOICES:
        RIPENING_MONTH_CHOICES_BACKWARDS[b] = a
setup_backwards_ripening()


class Command(BaseCommand):
    help = "Allows the importation of a Cultivar List."

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def handle(self, *args, **options):
        # Format of CSV:

        plants_kingdom = Kingdom.objects.get(name='Plants')

        with open(options['csv_file_path']) as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                genus, species_latin = row[0].split(' ')
                species_name = row[1]
                genus = self.__get_genus(plants_kingdom, genus)
                species = self.__get_species(genus, species_latin, species_name)
                cultivar = row[2]
                ripens_early = self.__parse_ripens(row[3])
                ripens_late = self.__parse_ripens(row[4])
                origin_year = self.__parse_origin_year(row[5])
                city = row[6]
                county = row[7]
                state = row[8]
                country = row[9]
                origin = self.__get_location(country, state, county, city)
                uses = self.__parse_uses(row[10])
                cultivar_obj = Cultivar.objects.filter(species=species, name=cultivar).first()
                adding = False
                if not cultivar_obj:
                    adding = True
                    cultivar_obj = Cultivar()
                    cultivar_obj.species = species
                    cultivar_obj.name = cultivar
                cultivar_obj.origin_year = origin_year
                cultivar_obj.origin_location = origin
                cultivar_obj.ripens_early = ripens_early
                cultivar_obj.ripens_late = ripens_late
                if adding:
                    print('Adding: {0}'.format(cultivar))
                else:
                    print('Updating : {0}'.format(cultivar))
                cultivar_obj.save()
                cultivar_obj.uses = uses
                cultivar_obj.save()


    def __get_genus(self, plants_kingdom, genus_name):
        obj = Genus.objects.filter(kingdom=plants_kingdom, latin_name=genus_name).first()
        if not obj:
            obj = Genus()
            obj.kingdom = plants_kingdom
            obj.name = 'Fix: ' + genus_name
            obj.latin_name = genus_name
            print('Creating Genus: ' + genus_name)
            obj.save()
        return obj

    def __get_species(self, genus, species_latin, species_name):
        obj = Species.objects.filter(genus=genus, latin_name=species_latin, name=species_name).first()
        if not obj:
            obj = Species()
            obj.genus = genus
            obj.name = species_name
            obj.latin_name = species_latin
            print('Creating Species: ' + species_name)
            obj.save()
        return obj

    def __does_cultivar_exists(self, species, cultivar_name):
        return Cultivar.objects.filter(species=species, name=cultivar_name).count() > 0

    def __parse_origin_year(self, origin_year):
        match = YEAR_RE.search(origin_year)
        year = None
        if match:
            year = int(match.group())
        return year

    def __parse_uses(self, use_line):
        # Format of uses
        #  b = Baking, c = cooking, j = juice, y = cider, d = drying, f = fresh eating, p = preserves
        uses = []
        for char in use_line:
            if char in USES:
                uses.append(USES[char])
        return uses

    def __get_location(self, country, state, county, city):
        if not country:
            return None
        if country == 'United States' or country == 'US':
            country = 'United States of America'
        if country == 'England':
            country = 'United Kingdom'
        try:
            country_obj = GeoModels.Country.objects.get(name=country)
            state_obj = None
            county_obj = None
            city_obj = None
            if county:
                county = county.replace(' County', '')
                county = county.replace(' Parish', '')
                county = county.replace(' Borough', '')
            if country == 'United States of America':
                if state:
                    state_obj = GeoModels.State.objects.get(country=country_obj, name=state)
                if county:
                    county_obj = GeoModels.County.objects.get(state=state_obj, name=county)
                if city:
                    city_obj = GeoModels.City.objects.get(state=state_obj, county=county_obj, name=city)
            location = GeoModels.Location.objects.filter(country=country_obj, state=state_obj, county=county_obj, city=city_obj).first()
            if not location:
                print('Creating Location: ')
                location = GeoModels.Location.objects.create(country=country_obj, state=state_obj, county=county_obj, city=city_obj)
        except Exception as e:
            print('Error during location: "{country}" "{state}" "{county}" "{city}"'.format(country=country, state=state, county=county, city=city))
            raise e
        return location


    def __parse_ripens(self, ripens_line):
        line = ripens_line.replace('.', '')
        line = line.replace('mid ', '')
        line = line.replace('Mid ', '')
        line = line.replace('late', 'Late')
        line = line.replace('early', 'Early')
        is_late = 'Late' in line
        is_early = 'Early' in line
        line = line.title()
        if not line:
            line = 'Unknown'
        return RIPENING_MONTH_CHOICES_BACKWARDS[line]


