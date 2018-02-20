import csv
from datetime import date
import re
from django.core.management.base import BaseCommand
from django_geo_db import models as GeoModels
from openfruit.taxonomy.models import Cultivar, Species
from openfruit.reports.disease.models import DiseaseType, DiseaseResistanceReport
from openfruit.fruit_reference.models import FruitReferenceType, FruitReference, Author

class Command(BaseCommand):
    help = "Imports a CAR resistant csv sheet."

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
                rust_resistance = row[1]
                url = row[2]
                author = row[3]
                title = row[4]
                date = row[5]
                type = row[6]

                reference_type, created = FruitReferenceType.objects.get_or_create(type=type)
                if created:
                    print('Created FruitReferenceType: ' + type)
                author_obj, created = Author.objects.get_or_create(name=author)
                if created:
                    print('Created Author: ' + author)
                reference, created = FruitReference.objects.get_or_create(
                    type=reference_type, title=title, url=url, author=author_obj, publish_date=date
                )
                if created:
                    print('Created FruitReference: ' + title)

                cultivar = Cultivar.objects.filter(species=apple, name=cultivar_name).first()
                if not cultivar:
                    cultivar = Cultivar()
                    cultivar.species = apple
                    cultivar.name = cultivar_name
                    cultivar.save()
                    print('Created Cultivar: ' + cultivar_name)
                if reference not in cultivar.fruitreference_set.all():
                    reference.cultivar_list.add(cultivar)
                    reference.save()
                    print('Added Cultivar to Reference: ' + cultivar.name)

                car_type, created = DiseaseType.objects.get_or_create(type='Cedar Apple Rust')
                if created:
                    print('Created DiseaseType: ' + 'Cedar Apple Rust')
                report, created = DiseaseResistanceReport.objects.get_or_create(
                    resistance_level=rust_resistance, disease_type=car_type, reference=reference,
                    cultivar=cultivar
                )
                if created:
                    print('Created DiseaseResistanceReport')



