from django.core.management.base import BaseCommand
from openfruit.reports.event.models import EventType

DEFAULT_TYPES = (
    ('Before Ripe', 'Pre-Ripened'),
    ('Bloom', 'Bloomed'),
    ('Bloom End', 'Blooms ended'),
    ('Dead', 'Died'),
    ('Dormant', 'Dormant'),
    ('Fruit Forming', 'Fruit formed'),
    ('Germination', 'Germinated'),
    ('Health Update', 'Health Updated'),
    ('Leaf Out', 'Leafed out'),
    ('New Growth', 'New growth'),
    ('Plant', 'Planted'),
    ('Ripe', 'Ripened'),
)


class Command(BaseCommand):
    help = "Syncs all event types."

    def handle(self, *args, **options):
        count = 0
        for type, passed in DEFAULT_TYPES:
            obj, created = EventType.objects.get_or_create(type=type, passed_tense=passed)
            if created:
                count +=1
        print('{0} types created.'.format(count))
