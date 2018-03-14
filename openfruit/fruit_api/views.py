from django.shortcuts import render
from django.conf import settings
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from django_geo_db.models import LocationMapType
from django_geo_db.services import LocationMapGenerator
from django_geo_db.serializers import LocationMapSerializer
from django_geo_db.services import GEO_DAL

from openfruit.common.views import EasyRestMixin
from openfruit.taxonomy.views import TaxonomyRestAPIMixin
from openfruit.fruit_api.services import FRUIT_API_SERVICE
from openfruit.taxonomy.serializers import CultivarSerializer
from openfruit.reports.disease.services import DISEASE_SERVICE
from openfruit.reports.review.services import FRUIT_REVIEW_DAL
from openfruit.taxonomy.services import TAXONOMY_DAL



class CultivarQuery(APIView, EasyRestMixin, TaxonomyRestAPIMixin):
    """
    Queries for full information on cultivars.
    This has two forms.
    1. As a single cultivar.
    2. As multiple cultivars.

    Single:
    /api/v1/fruits/cultivars/?species=Malus domestica&cultivar=Red Rebel
    /api/v1/fruits/cultivars/?sc_1=Malus domestica,Red Rebel&sc_2=Malus domestica,Aunt Rachel

    &addons=[location,review,resistance]
    &review_types=[sweet,sour,firm,bitter,juicy,rating]
    &review_metrics=[avg,max,min]
    """

    def get(self, request):
        print(len(connection.queries))
        if 'sc_1' in request.query_params:
            result = self.__handle_many(request)
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
        return result[0]

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
