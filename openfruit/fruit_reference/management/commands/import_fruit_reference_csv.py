import csv
from django.core.management.base import BaseCommand
from openfruit.taxonomy.models import Cultivar, Species
from openfruit.fruit_reference.models import FruitReferenceType, FruitReference, Author

class Command(BaseCommand):
    help = "Imports a csv sheet of cultivars for a reference.."

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def handle(self, *args, **options):
        apple = Species.objects.get(latin_name='Malus domestica')

        with open(options['csv_file_path']) as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                cultivar_name = row[0]
                reference_id = row[1]

                reference = FruitReference.objects.get(pk=reference_id)
                print(cultivar_name)
                cultivar, created = Cultivar.objects.get_or_create(species=apple, name=cultivar_name)
                if created:
                    print('Created Cultivar: ' + cultivar_name)
                if reference not in cultivar.fruitreference_set.all():
                    reference.cultivar_list.add(cultivar)
                    reference.save()



