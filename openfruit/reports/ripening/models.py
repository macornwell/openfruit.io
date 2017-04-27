from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField
from openfruit.geography.models import GeoCoordinate
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class FruitRipeningReport(models.Model, CultivarSpeciesMixin):
    fruit_ripening_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    how_old_is_plant = IntegerRangeField(min_value=1, max_value=500)
    was_auto_generated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.validate_species_cultivar()
        super(FruitRipeningReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1} Ripening'.format(self.datetime, obj.name)


auditlog.register(FruitRipeningReport)
