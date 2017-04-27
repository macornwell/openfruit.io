from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.geography.models import GeoCoordinate
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class BloomReport(models.Model, CultivarSpeciesMixin):
    """
    A reports that states that a particular species or cultivar is blooming.
    """
    bloom_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    is_profuse = models.BooleanField(default=False)
    was_auto_generated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.validate_species_cultivar()
        super(BloomReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        if self.is_profuse:
            return '{0} - {1} bloomed profusely.'.format(self.datetime, obj.name)
        return '{0} - {1} bloomed.'.format(self.datetime, obj.name)


auditlog.register(BloomReport)
