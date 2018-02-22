import csv
from django.core.management.base import BaseCommand
from openfruit.taxonomy.models import Cultivar, Species
from openfruit.fruit_reference.models import FruitReferenceType, FruitReference, Author

class Command(BaseCommand):
    help = "Fixes duplicate fruit references by consolidating them into the lowest ID."

    def handle(self, *args, **options):
        apple = Species.objects.get(latin_name='Malus domestica')
        reference_to_author_to_list = {}
        for f in FruitReference.objects.all():
            if f.title not in reference_to_author_to_list:
                reference_to_author_to_list[f.title] = {}
            if f.author not in reference_to_author_to_list[f.title]:
                reference_to_author_to_list[f.title][f.author] = []
            reference_to_author_to_list[f.title][f.author].append(f)
        for title in reference_to_author_to_list:
            for author in reference_to_author_to_list[title]:
                reference_list = sorted(reference_to_author_to_list[title][author], key=lambda x: x.fruit_reference_id)
                if len(reference_list) > 1:
                    lowest = reference_list[0]
                    for idx in range(1, len(reference_list)):
                        to_remove = reference_list[idx]
                        for cultivar in to_remove.cultivar_list.all():
                            print('Moving {0} from {1} to {2}'.format(str(cultivar), str(to_remove), str(lowest)))
                            lowest.cultivar_list.add(cultivar)
                        lowest.save()
                        print('Deleting: {0}'.format(to_remove))
                        to_remove.delete()
                else:
                    print('Skipping: ' + str(reference_list))
                    pass  # Don't need to do anything because there is only one reference.






