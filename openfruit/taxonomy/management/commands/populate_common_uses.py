from django.core.management.base import BaseCommand
from openfruit.taxonomy.models import FruitUsageType

COMMON_USES = [
    'Baking',
    'Cooking',
    'Cider',
    'Drying',
    'Fresh Eating',
    'Juice',
    'Preserves',
    'Storage',
]


class Command(BaseCommand):
    help = "Creates all of the default Fruit Uses."

    def handle(self, *args, **options):
        for use in COMMON_USES:
            obj, made = FruitUsageType.objects.get_or_create(type=use)
            if made:
                print('Created {0}'.format(use))
