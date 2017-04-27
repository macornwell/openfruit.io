from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.geography.models import GeoCoordinate
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.taxonomy.validators import CultivarSpeciesMixin

AFFINITY_BAD = -1
AFFINITY_NEUTRAL = 0
AFFINITY_GOOD = 1

AFFINITY_CHOICES = (
    (AFFINITY_BAD, 'Bad'),
    (AFFINITY_NEUTRAL, 'Neutral'),
    (AFFINITY_GOOD, 'Good'),
)


class EventImage(models.Model):
    event_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='event-images')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)


class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    passed_tense = models.CharField(max_length=20, help_text='The passed tense of the event word. Example: Bloomed')


class EventReport(models.Model, CultivarSpeciesMixin):
    event_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    was_auto_generated = models.BooleanField(default=False)
    event_type = models.ForeignKey(EventType)
    affinity = models.IntegerField(choices=AFFINITY_CHOICES, default=AFFINITY_NEUTRAL)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.validate_species_cultivar()
        super(EventReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1}.'.format(self.datetime, obj.name)


auditlog.register(EventReport)
auditlog.register(EventType)
auditlog.register(EventImage)
