from django.db import models
from openfruit.taxonomy.models import Cultivar, Species


class FruitReferenceType(models.Model):
    fruit_reference_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class FruitReference(models.Model):
    """
    A reference about a fruit. Book, newspaper article, url, etc.
    """
    fruit_reference_id = models.AutoField(primary_key=True)
    species_list = models.ManyToManyField(Species, blank=True)
    cultivar_list = models.ManyToManyField(Cultivar, blank=True)
    title = models.CharField(max_length=100)
    reference = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    type = models.ForeignKey(FruitReferenceType)
    author = models.ForeignKey(Author)
    publish_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (('title', 'type', 'author'),)

    def __str__(self):
        return self.title

