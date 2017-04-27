from django.core.management.base import BaseCommand
from openfruit.taxonomy.services import generate_default_genus_entries
from openfruit.taxonomy.models import PLANT_KINGDOM_NAMES, Kingdom, Genus



class Command(BaseCommand):
    help = "Creates all of the default taxonomy objects."

    def handle(self, *args, **options):
        print('Looking at Kingdoms')
        commonName, latinName = PLANT_KINGDOM_NAMES
        plantKingdom, created = Kingdom.objects.get_or_create(name=commonName, latin_name=latinName)
        if created:
            print('Created Plant Kingdom')
        print('Looking at Genus')
        for commonName, latinName in generate_default_genus_entries():
            obj, created = Genus.objects.get_or_create(kingdom=plantKingdom, name=commonName, latin_name=latinName)
            if created:
                print('Created Genus "{0}"'.format(latinName))
        print('Done.')
