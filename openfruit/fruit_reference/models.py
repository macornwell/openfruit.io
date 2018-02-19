from django.db import models
from openfruit.taxonomy.models import Cultivar, Species


class FruitReferenceType(models.Model):
    fruit_reference_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10)


class FruitReference(models.Model):
    """
    A reference about a fruit. Book, newspaper article, url, etc.
    """
    fruit_reference_id = models.AutoField(primary_key=True)
    species_list = models.ManyToManyField(Species)
    cultivar_list = models.ManyToManyField(Cultivar)
    reference = models.TextField()
    type = models.ForeignKey(FruitReferenceType)
    author = models.CharField(max_length=50, null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('reference', 'type'))

