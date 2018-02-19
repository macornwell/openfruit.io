from django.shortcuts import render
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


from openfruit.taxonomy.serializers import CultivarSerializer
from openfruit.fruit_search.services import FRUIT_SEARCH_SERVICE
from openfruit.taxonomy.models import COMMON_USES, RIPENING_MONTH_CHOICES
from django_geo_db.services import GEO_DAL
from openfruit.fruit_reference.services import FRUIT_REFERENCE_SERVICE

from rest_framework.generics import ListAPIView

def fruit_search(request):
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    data = {
        'USES': COMMON_USES,
        'BOOK_REFERENCES': FRUIT_REFERENCE_SERVICE.get_book_references(),
        'RIPENINGS': RIPENING_MONTH_CHOICES,
        'STATES': GEO_DAL.get_us_states(),
        'TOKEN': token,
    }
    return render(request, template_name='fruit_search/search-and-filter.html', context=data)

class FruitSearchListView(ListAPIView):
    serializer_class = CultivarSerializer

    def get_queryset(self):
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
        reference_id = []
        if books:
            for book in books:
                reference_id.append(book)
        results = FRUIT_SEARCH_SERVICE.filter(
            species=species, state=state, use_list=use_list,
            year_low=year_low, year_high=year_high, ripening_low=ripening_low,
            ripening_high=ripening_high, reference_id=reference_id
        )
        return results
