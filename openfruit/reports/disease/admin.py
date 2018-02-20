from django.contrib import admin
from openfruit.reports.disease.models import DiseaseResistanceReport, DiseaseType

# Register your models here.
admin.site.register(DiseaseType)
admin.site.register(DiseaseResistanceReport)
