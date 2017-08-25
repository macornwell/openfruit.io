import os.path
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from sorl.thumbnail.fields import ImageField
from openfruit.geography.models import Location
from openfruit.taxonomy.models import FruitingPlant
from openfruit.taxonomy.validators import CultivarSpeciesMixin

AFFINITY_BAD = -1
AFFINITY_NEUTRAL = 0
AFFINITY_GOOD = 1

AFFINITY_CHOICES = (
    (AFFINITY_BAD, 'Bad'),
    (AFFINITY_NEUTRAL, 'Neutral'),
    (AFFINITY_GOOD, 'Good'),
)

DIED_TYPE = 'Died'

EVENT_TYPES = (
    ('Blooming', 'Bloomed'),
    ('Bloom Finished', 'Blooms ended'),
    (DIED_TYPE, DIED_TYPE),
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


class EventReport(models.Model):
    event_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(default=timezone.now)
    fruiting_plant = models.ForeignKey(FruitingPlant)
    was_auto_generated = models.BooleanField(default=False)
    event_type = models.ForeignKey(EventType)
    affinity = models.IntegerField(choices=AFFINITY_CHOICES, default=AFFINITY_NEUTRAL)
    notes = models.TextField(blank=True, null=True)
    image = ImageField(upload_to=upload_image, blank=True, null=True)

    def __str__(self):
        value = '{0} - {1} - {2}'.format(self.datetime, self.event_type, str(self.fruiting_plant))
        return value


auditlog.register(EventReport)
auditlog.register(EventType)
