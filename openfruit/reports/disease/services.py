from openfruit.reports.disease.models import DiseaseType, DiseaseResistanceReport


class DiseaseService:

    def get_disease_types(self):
        return DiseaseType.objects.all().values_list('type', flat=True).order_by()

    def get_disease_resistance_types_for_cultivar(self, cultivar):
        values = DiseaseResistanceReport.objects.filter(cultivar=cultivar, resistance_level='e').values('disease_type').distinct()
        values = DiseaseType.objects.filter(disease_type_id__in=values).values_list('type', flat=True)
        return values

DISEASE_SERVICE = DiseaseService()
