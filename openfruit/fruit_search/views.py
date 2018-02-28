from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings

from rest_framework_jwt.settings import api_settings
from rest_framework.generics import ListAPIView

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from openfruit.geography.services import GEOGRAPHY_DAL
from openfruit.taxonomy.serializers import CultivarSerializer
from openfruit.fruit_search.services import FRUIT_SEARCH_SERVICE
from openfruit.taxonomy.models import COMMON_USES, RIPENING_MONTH_CHOICES, CHROMOSOME_CHOICES
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.fruit_reference.services import FRUIT_REFERENCE_SERVICE
from openfruit.reports.disease.services import DISEASE_SERVICE


def fruit_search(request):
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    uses = [a for a in COMMON_USES]
    uses.append('Other')
    data = {
        'USES': uses,
        'BOOK_REFERENCES': FRUIT_REFERENCE_SERVICE.get_book_references(),
        'RIPENINGS': RIPENING_MONTH_CHOICES,
        'STATES': GEOGRAPHY_DAL.get_states_with_fruits(),
        'TOKEN': token,
        'CHROMOSOMES': [c[0] for c in CHROMOSOME_CHOICES],
        'DISEASE_TYPES': DISEASE_SERVICE.get_disease_types(),
        'SPECIES': TAXONOMY_DAL.get_all_species_with_cultivars(),
        'OF_API_USERNAME': settings.OF_API_USERNAME,
        'OF_API_PASSWORD': settings.OF_API_PASSWORD,
    }
    return render(request, template_name='fruit_search/search-and-filter.html', context=data)


class FruitSearchListView(ListAPIView):
    serializer_class = CultivarSerializer

    def _unpack_query(self, query_list):
        data = query_list.split('$')
        queries = {}
        if not data:
            return queries
        for d in data:
            if not d:
                continue
            key, value = d.split('=')
            if ',' in value:
                values = value.split(',')
                value_list = []
                for v in values:
                    if not v:
                        continue
                    value_list.append(v)
                queries[key] = value_list
            else:
                queries[key] = value
        return queries

    def get_queryset(self):
        params = self.request.query_params
        all_queries = []
        for key in params:
            if key.startswith('query'):
                queries = self._unpack_query(params[key])
                all_queries.append(queries)
        url = self.request.build_absolute_uri
        result = cache.get(url)
        if result:
            pass
        else:
            result = FRUIT_SEARCH_SERVICE.filter_multiple_queries(all_queries)
            cache.set(url, result)
        return result


    def old_get_queryset(self):
        params = self.request.query_params
        species = params.get('species', None)
        state = params.get('state', None)
        uses = params.get('uses', [])
        use_list = []
        if uses:
            for obj in uses.split(','):
                use_list.append(obj)
        year_low = params.get('year_low', None)
        year_high = params.get('year_high', None)
        ripening_low = params.get('ripening_low', None)
        ripening_high = params.get('ripening_high', None)
        books = params.get('books', None)
        chromosomes = params.get('chromosomes', None)
        resistances = params.get('resistances', [])
        resistance_list = []
        if resistances:
            for r in resistances.split(','):
                resistance_list.append(r)
        reference_id = []
        if books:
            for book in books.split(','):
                reference_id.append(book)
        results = FRUIT_SEARCH_SERVICE.filter(
            species=species, state=[state,], use_list=use_list,
            year_low=year_low, year_high=year_high, ripening_low=ripening_low,
            ripening_high=ripening_high, references=reference_id, chromosomes=chromosomes,
            resistances=resistance_list,
        )
        return results

