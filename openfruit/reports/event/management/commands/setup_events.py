from django.core.management.base import BaseCommand
from openfruit.reports.event.models import EventType, EVENT_TYPES




class Command(BaseCommand):
    help = "Syncs all event types."

    def handle(self, *args, **options):
        count = 0
        for type, passed in EVENT_TYPES:
            obj, created = EventType.objects.get_or_create(type=type, passed_tense=passed)
            if created:
                count +=1
        print('{0} types created.'.format(count))
