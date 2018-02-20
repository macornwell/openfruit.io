from django.db import models
from openfruit.fruit_reference.models import FruitReference
from openfruit.taxonomy.models import Cultivar

DISEASE_RESISTANCE_CHOICES = (
    ('p', 'Poor'),
    ('f', 'Fair'),
    ('e', 'Excellent'),
)


class DiseaseType(models.Model):
    disease_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=25)


class DiseaseResistanceReport(models.Model):
    disease_resistance_report_id = models.AutoField(primary_key=True)
    disease_type = models.ForeignKey(DiseaseType)
    resistance_level = models.CharField(max_length=1, choices=DISEASE_RESISTANCE_CHOICES)
    reference = models.ForeignKey(FruitReference, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar)

