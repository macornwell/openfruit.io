import csv
from datetime import date
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from openfruit.taxonomy.models import Cultivar, Species
from openfruit.reports.review.models import FruitReview

class Command(BaseCommand):
    help = "Imports a CAR resistant csv sheet."

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str)

    def handle(self, *args, **options):

        with open(options['csv_file_path']) as f:
            reader = csv.reader(f)
            first = True
            for row in reader:
                if first:
                    first = False
                    continue
                try:
                    username = row[0]
                    user = User.objects.get(username__iexact=username)
                    species = row[1]
                    species = Species.objects.get(latin_name__iexact=species)
                    cultivar = row[2]
                    cultivar = Cultivar.objects.get(name__iexact=cultivar)
                    sweet = row[3]
                    sour = row[4]
                    bitter = row[5]
                    juicy = row[6]
                    firm = row[7]
                    was_picked_early = row[8]
                    rating = row[9]
                    review = FruitReview()
                    review.cultivar = cultivar
                    review.submitted_by = user
                    review.species = species
                    review.sweet = sweet
                    review.sour = sour
                    review.bitter = bitter
                    review.juicy = juicy
                    review.firm = firm
                    if was_picked_early:
                        review.was_picked_early = was_picked_early
                    if rating:
                        review.rating = rating
                    print('Creating: {0}'.format(review))
                    review.save()
                except Exception as e:
                    print(row)
                    raise e

