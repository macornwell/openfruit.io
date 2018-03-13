from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView

from openfruit.common.views import EasyRestMixin
from openfruit.reports.disease.models import DiseaseType
from openfruit.reports.disease.serializers import DiseaseTypeSerializer
from openfruit.reports.disease.services import DISEASE_SERVICE
from openfruit.taxonomy.models import Cultivar
from openfruit.taxonomy.views import TaxonomyRestAPIMixin
from openfruit.taxonomy.services import TAXONOMY_DAL


class DiseaseTypeListView(EasyRestMixin, ListAPIView):
    queryset = DiseaseType.objects.all()
    serializer_class = DiseaseTypeSerializer

    def get_queryset(self):
        return DiseaseType.objects.all()


class DiseaseResistancesView(APIView, TaxonomyRestAPIMixin, EasyRestMixin):
    pagination_class = None

    def get(self, request):
        species, cultivar = self.get_species_and_cultivar(request)
        cultivar = TAXONOMY_DAL.get_cultivar(species, cultivar)
        disease_resistances = DISEASE_SERVICE.get_disease_resistance_types_for_cultivar(cultivar)
        return Response(disease_resistances)
