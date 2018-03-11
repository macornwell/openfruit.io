from rest_framework.views import APIView, Response
from rest_framework.exceptions import ParseError
from openfruit.common.views import EasyRestMixin
from openfruit.reports.review import models, serializers
from openfruit.reports.review.services import FRUIT_REVIEW_DAL

# Create your views here.


class FruitReviewView(APIView, EasyRestMixin):
    """
    A review for a single cultivar of fruit.
    The more specific the review the faster the query.
    Regardless of filtering, all types are in the form of an array.

    Only what is requested is returned.

    Optional parameters separated separated by commas for multiple.
    :parameter
    ?types=[sweet,sour,firm,bitter,juicy,rating]
    ?metrics=[average,max,min]


    :returns
    Example: Everything
    /api/v1/reports/review/?cultivar=Anna&species=Apple
    {
        max : [
            'sweet': 10,
            'sour': 10,
            'firm': 10,
            'bitter': 10,
            'juicy': 10,
            'rating': 5,
        ],
        average : [
            'sweet': 5,
            'sour': 5,
            'firm': 5,
            'bitter': 5,
            'juicy': 5,
            'rating': 3,
        ],
        min : [
            'sweet': 1,
            'sour': 1,
            'firm': 1,
            'bitter': 1,
            'juicy': 1,
            'rating': 1,
        ]
    }

    Example: Two Types
    /api/v1/reports/review/?cultivar=Anna&species=Apple&types=sweet,sour
    {
        max : [
            'sweet': 10,
            'sour': 10,
        ],
        average : [
            'sweet': 5,
            'sour': 5,
        ],
        min : [
            'sweet': 1,
            'sour': 1,
        ]
    }

    If one metric and one type is requested only the value is returned.
    /api/v1/reports/review/?cultivar=Anna&species=Apple&metrics=average&types=sour
    {
        9
    }

    If one metric is requested the types are turned.
    /api/v1/reports/review/?cultivar=Anna&species=Apple&metrics=average
    {
        'sweet': 1,
        'sour': 1,
        'firm': 1,
        'bitter': 1,
        'juicy': 1,
        'rating': 1,
    }

    """
    pagination_class = None

    def get(self, request):
        species = request.query_params.get('species', None)
        if not species:
            raise ParseError('Error: species')
        cultivar = request.query_params.get('cultivar', None)
        if not cultivar:
            raise ParseError('Error: cultivar')

        types = self.parse_array_query_params(request, 'types')
        metrics = self.parse_array_query_params(request, 'metrics')
        result = FRUIT_REVIEW_DAL.get_averages_for_cultivar(species, cultivar, types=types, metrics=metrics)
        if len(result) == 1:
            values = list(result.values())
            value = values[0]
            if len(value) == 1:
                value = list(value.values())[0]
                return Response(value)
            else:
                return Response(value)
        return Response(result)
