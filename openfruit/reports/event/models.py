import os.path
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from sorl.thumbnail.fields import ImageField
from openfruit.geography.models import Location
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

EVENT_TYPES = (
    ('Blooming', 'Bloomed'),
    ('Bloom Finished', 'Blooms ended'),
    ('Died', 'Died'),
    ('Dormant', 'Dormant'),
    ('Fruit Forming', 'Fruit formed'),
    ('Germination', 'Germinated'),
    ('Health Update', 'Health Updated'),
    ('Leafing Out', 'Leafed out'),
    ('New Growth', 'New growth'),
    ('Just Planted', 'Planted'),
    ('Ripening', 'Ripened'),
)


def upload_image(instance, filename):
    return os.path.join('event-images', instance.submitted_by.username, filename)


class EventType(models.Model):
    event_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    passed_tense = models.CharField(max_length=20, help_text='The passed tense of the event word. Example: Bloomed')

    def __str__(self):
        return self.type


class EventReport(models.Model, CultivarSpeciesMixin):
    event_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    was_auto_generated = models.BooleanField(default=False)
    event_type = models.ForeignKey(EventType)
    affinity = models.IntegerField(choices=AFFINITY_CHOICES, default=AFFINITY_NEUTRAL)
    notes = models.TextField(blank=True, null=True)
    image = ImageField(upload_to=upload_image, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.prepare_for_save()
        super(EventReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1}.'.format(self.datetime, obj.name)


auditlog.register(EventReport)
auditlog.register(EventType)
