from openfruit.reports.disease.models import DiseaseType


class DiseaseService:

    def get_disease_types(self):
        return DiseaseType.objects.all().values_list('type', flat=True).order_by()

DISEASE_SERVICE = DiseaseService()
