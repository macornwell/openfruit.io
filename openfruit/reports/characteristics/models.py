from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.geography.models import GeoCoordinate
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class FruitCharacteristicReport(models.Model, CultivarSpeciesMixin):
    fruit_characteristic_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    sweet = IntegerRangeField(min_value=1, max_value=10)
    sour = IntegerRangeField(min_value=1, max_value=10)
    bitter = IntegerRangeField(min_value=1, max_value=10, default=1)
    juicy = IntegerRangeField(min_value=1, max_value=10)
    firm = IntegerRangeField(min_value=1, max_value=10)
    was_picked_early = models.BooleanField(default=False)
    was_auto_generated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.validate_species_cultivar()
        super(FruitCharacteristicReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1} rating.'.format(self.datetime, obj.name, self.submitted_by.username, self.rating)


auditlog.register(FruitCharacteristicReport)