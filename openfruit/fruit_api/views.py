from django.conf import settings
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from django_geo_db.models import Country, State, City, Region, County

from openfruit.common.views import EasyRestMixin
from openfruit.taxonomy.views import TaxonomyRestAPIMixin
from openfruit.taxonomy.models import Species
from openfruit.fruit_api.services import FRUIT_API_SERVICE


class CultivarQuery(APIView, EasyRestMixin, TaxonomyRestAPIMixin):
    """
    Queries for full information on cultivars.
    This has two forms.
    1. As a single cultivar.
    2. As multiple cultivars.

    Single:
    /api/v1/fruits/cultivars/?species=Malus domestica&cultivar=Red Rebel

    Multiple:
    /api/v1/fruits/cultivars/?sc_1=Malus domestica,Red Rebel&sc_2=Malus domestica,Aunt Rachel

    Multi-Geo:
    /api/v1/fruits/cultivars/?species=Malus domestica&country=United States of America&state=Georgia

    &addons=[location,review,resistances]
    &review_types=[sweet,sour,firm,bitter,juicy,rating]
    &review_metrics=[avg,max,min]
    """

    def get(self, request):
        print(len(connection.queries))
        if 'sc_1' in request.query_params:
            result = self.__handle_many(request)
        elif 'country' in request.query_params:
            result = self.__handle_geo_many(request)
        else:
            result = self.__handle_single(request)
        print(len(connection.queries))
        return Response(result)

    def __process_location_maps(self, request, results):
        for r in results:
            url = r['location']['map_file_url']
            if url and 'static' not in url:
                url = request.build_absolute_uri(settings.MEDIA_URL + url)
                r['location']['map_file_url'] = url

    def __handle_single(self, request):
        species, cultivar = self.get_species_and_cultivar(request)
        addons = self.parse_array_query_params(request, 'addons')
        review_types = self.parse_array_query_params(request, 'review_types')
        review_metrics = self.parse_array_query_params(request, 'review_metrics')
        result = FRUIT_API_SERVICE.full_cultivar_query(species, cultivar, addons=addons, review_types=review_types, review_metrics=review_metrics)
        if 'location' in addons:
            self.__process_location_maps(request, [result,])
        return result

    def __handle_many(self, request):
        species_and_cultivars = []
        for key in request.query_params:
            try:
                if key.startswith('sc_'):
                    species, cultivar = self.parse_array_query_params(request, key)
                    species_and_cultivars.append((species, cultivar))
            except Exception as e:
                print(key)
                raise e
        addons = self.parse_array_query_params(request, 'addons')
        review_types = self.parse_array_query_params(request, 'review_types')
        review_metrics = self.parse_array_query_params(request, 'review_metrics')
        result = FRUIT_API_SERVICE.full_cultivar_query_many(species_and_cultivars, addons=addons, review_types=review_types, review_metrics=review_metrics)
        if 'location' in addons:
            self.__process_location_maps(request, result)
        return result

    def __handle_geo_many(self, request):
        country = request.query_params['country']
        state = request.query_params.get('state', None)
        county = request.query_params.get('county', None)
        city = request.query_params.get('city', None)
        region = request.query_params.get('region', None)
        species = request.query_params.get('species', None)

        country = Country.objects.get(name__iexact=country)
        if region:
            region = Region.objects.get(country=country, name__iexact=region)
        if state:
            state = State.objects.get(name__iexact=state)
        if county:
            county = County.objects.get(state=state, name__iexact=county)
        if city:
            city = City.objects.get(state=state, name__iexact=city)
        if species:
            species = Species.objects.get(latin_name__iexact=species)

        addons = self.parse_array_query_params(request, 'addons')
        if not 'location' in addons:
            addons.append('location')
        review_types = self.parse_array_query_params(request, 'review_types')
        review_metrics = self.parse_array_query_params(request, 'review_metrics')

        result = FRUIT_API_SERVICE.full_cultivar_query_geo(country, region=region, state=state, county=county,
                                                           city=city, species=species, addons=addons,
                                                           review_types=review_types, review_metrics=review_metrics)
        if 'location' in addons:
            self.__process_location_maps(request, result)
        return result
