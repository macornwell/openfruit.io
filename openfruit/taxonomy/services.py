import os
import csv
from django.db.models import Q
from openfruit.settings import BASE_DIR
from openfruit.taxonomy.models import Species, Genus, Cultivar, FruitingPlant
from openfruit.geography.models import GeoCoordinate



class TaxonomyDAL:

    def public_plants_query(self, user, queryArgs):
        qs = FruitingPlant.objects.filter(is_private=False)
        if 'no-user' in queryArgs:
            qs = qs.exclude(user_manager=user)
        if 'species' in queryArgs:
            speciesID = queryArgs['species']
            qs = qs.filter(species=speciesID)
        if 'show-dead-only' in queryArgs:
            qs = qs.filter(date_died__isnull=False)
        else:
            qs = qs.filter(date_died__isnull=True)
        return qs

    def query_users_fruiting_plants(self, user, species=None):
        objects = FruitingPlant.objects.get_plants_for_user(user)
        if species:
            objects.filter(species=species)
        return objects


    def get_all_species_with_fruiting_plants(self):
        speciesUsed = FruitingPlant.objects.order_by('species').values('species').distinct()
        return Species.objects.filter(species_id__in=speciesUsed)

    def get_all_species_with_fruiting_plants_of_user(self, user):
        speciesUsed = FruitingPlant.objects.filter(user_manager=user).order_by('species').values('species').distinct()
        return Species.objects.filter(species_id__in=speciesUsed)

    def get_fruiting_plant_by_id(self, id):
        return FruitingPlant.objects.get(pk=id)

    def get_genus_by_name(self, name):
        return Genus.objects.get(Q(name__iexact=name) | Q(latin_name__iexact=name))

    def move_fruiting_plant(self, fruitingPlantID, lat, lon):
        plant = FruitingPlant.objects.get(pk=fruitingPlantID)
        coord = plant.geocoordinate
        coord.lat = lat
        coord.lon = lon
        coord.save()

    def generate_default_genus_entries(self):
        """
        Returns a list of (common name, latin name)
        :return:
        """
        with open(os.path.join(BASE_DIR, 'openfruit', 'taxonomy', 'default_genus.csv')) as file:
            reader = csv.DictReader(file)
            for row in reader:
                commonName = row['common_name'].strip()
                latinName = row['latin_name'].strip()
                yield (commonName, latinName)

    def get_genus_to_species_count(self):
        """
        Gets a dictionary of genus primary keys to the number of species that have that genus.
        If a genus has no species associated with it, it will be in the dictionary as a 0.
        :return:
        """
        tupleList = Species.objects.filter(genus_id__isnull=False).values_list('genus_id', 'species_id')
        dict = {}
        for genusID, speciesID in tupleList:
            if genusID not in dict:
                dict[genusID] = 0
            dict[genusID] += 1
        idList = Genus.objects.all().values_list('genus_id')
        for tuple in idList:
            id = tuple[0]
            if id not in dict:
                dict[id] = 0
        return dict

    def get_cultivars_by_species(self, species):
        return Cultivar.objects.filter(species=species)

    def get_species_by_name(self, name):
        return Species.objects.get(Q(name__iexact=name) | Q(latin_name__iexact=name))

TAXONOMY_DAL = TaxonomyDAL()