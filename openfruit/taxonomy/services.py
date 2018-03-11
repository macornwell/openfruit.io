import os
import csv
from django.db.models import Q
from openfruit.settings import BASE_DIR
from openfruit.taxonomy.models import Species, Genus, Cultivar, FruitingPlant
from django_geo_db.models import GeoCoordinate
from django_geo_db.utilities import BoundingBox, LatLon, GeoResolutionAlgorithm



class TaxonomyDAL:

    def get_all_species_with_cultivars(self):
        species_id_list = Cultivar.objects.order_by('species').values('species_id').distinct()
        species = Species.objects.filter(species_id__in=species_id_list)
        return species

    def get_cultivar_count(self):
        return Cultivar.objects.count()

    def get_fruiting_plants_created_by(self, user):
        return FruitingPlant.objects.filter(created_by=user)

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
        speciesUsed = FruitingPlant.objects.filter(created_by=user).order_by('species').values('species').distinct()
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

    def get_cultivar(self, species, cultivar_name):
        """
        Gets a cultivar.
        Species name can either be in latin or the common name. IExact is for both.
        :param species:
        :param cultivar_name:
        :return:
        """
        return Cultivar.objects.filter(name=cultivar_name).filter(Q(species__name__iexact=species) | Q(species__latin_name__iexact=species)).first()

    def get_cultivar_by_id(self, cultivar_id):
        return Cultivar.objects.get(pk=cultivar_id)

    def get_species_by_name(self, name):
        return Species.objects.get(Q(name__iexact=name) | Q(latin_name__iexact=name))

    def get_species_by_id(self, species_id):
        return Species.objects.get(pk=species_id)

    def query_fruiting_plants(self, query_params):
        north_east = query_params.get('north_east', None)
        south_west = query_params.get('south_west', None)
        if not north_east and not south_west:
            raise Exception('Must have a bounding box.')
        species = query_params.get('species', None)
        ne = LatLon.parse_string(north_east)
        sw = LatLon.parse_string(south_west)
        bounding_box = BoundingBox(ne, sw)
        nw = bounding_box.get_north_west()
        alg = GeoResolutionAlgorithm(bounding_box)

        query = FruitingPlant.objects.all()

        lat_result = alg.lat_db_resolution()
        kwargs = {
        }
        if lat_result:
            # Macro Filtering for filtering the vast majority of non-matches.
            args = [
                'geocoordinate__lat_tens',
                'geocoordinate__lat_ones',
                'geocoordinate__lat_tenths',
                'geocoordinate__lat_hundredths',
                'geocoordinate__lat_thousands',
                'geocoordinate__lat_ten_thousands',
                #'geocoordinate__lat_ten_hundred_thousands',
            ]
            # Is this negative?
            if lat_result[0]:
                kwargs['geocoordinate__lat_neg'] = True
            else:
                kwargs['geocoordinate__lat_neg'] = False
            for i in range(1, len(lat_result)):
                if lat_result[i] > -1:
                    kwargs[args[i - 1]] = lat_result[i]
        lon_result = alg.lon_db_resolution()
        if lon_result:
            args = [
                'geocoordinate__lon_hundreds',
                'geocoordinate__lon_tens',
                'geocoordinate__lon_ones',
                'geocoordinate__lon_tenths',
                'geocoordinate__lon_hundredths',
                'geocoordinate__lon_thousands',
                'geocoordinate__lon_ten_thousands',
                #'geocoordinate__lon_hundred_thousands',
            ]
            # Is this negative?
            if lon_result[0]:
                kwargs['geocoordinate__lon_neg'] = True
            else:
                kwargs['geocoordinate__lon_neg'] = False
            for i in range(1, len(lon_result)):
                if lon_result[i] > -1:
                    kwargs[args[i - 1]] = lon_result[i]

        query = query.filter(**kwargs)
        # Simple Query which cleans anything else out.
        query = query.filter(geocoordinate__lat__lte=nw.lat, geocoordinate__lat__gte=sw.lat,
                             geocoordinate__lon__lte=ne.lon, geocoordinate__lon__gte=nw.lon)

        return query

    def get_species_with_google_maps_images(self):
        return Species.objects.filter(Q(google_maps_image_url__isnull=False) & ~Q(google_maps_image_url=''))








TAXONOMY_DAL = TaxonomyDAL()
