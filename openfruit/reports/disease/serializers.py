from rest_framework import serializers
from openfruit.reports.disease.models import DiseaseType


class DiseaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseType
        fields = ('type',)
