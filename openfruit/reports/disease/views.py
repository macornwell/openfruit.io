from rest_framework.generics import ListAPIView

from openfruit.common.views import EasyRestMixin
from openfruit.reports.disease.models import DiseaseType
from openfruit.reports.disease.serializers import DiseaseTypeSerializer


class DiseaseTypeListView(EasyRestMixin, ListAPIView):
    queryset = DiseaseType.objects.all()
    serializer_class = DiseaseTypeSerializer

    def get_queryset(self):
        return DiseaseType.objects.all()

