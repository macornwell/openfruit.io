from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField
from openfruit.geography.models import GeoCoordinate
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class FruitReviewReport(models.Model, CultivarSpeciesMixin):
    """
    A freeform review for a piece of fruit.
    """
    fruit_review_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    rating = IntegerRangeField(min_value=1, max_value=5)
    text = models.TextField(max_length=1000)

    def save(self, *args, **kwargs):
        self.validate_species_cultivar()
        super(FruitReviewReport, self).save(*args, **kwargs)


    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1} - {2} Gives a {3} of 5 rating.'.format(self.datetime, obj.name, self.submitted_by.username, self.rating)

auditlog.register(FruitReviewReport)
