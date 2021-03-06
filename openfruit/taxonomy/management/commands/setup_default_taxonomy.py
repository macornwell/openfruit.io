from django.core.management.base import BaseCommand
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.taxonomy.models import PLANT_KINGDOM_NAMES, Kingdom, Genus



class Command(BaseCommand):
    help = "Creates all of the default taxonomy objects."

    def handle(self, *args, **options):
        self.populate()

    def populate(self):
        print('Looking at Kingdoms')
        commonName, latinName = PLANT_KINGDOM_NAMES
        plantKingdom, created = Kingdom.objects.get_or_create(name=commonName, latin_name=latinName)
        if created:
            print('Created Plant Kingdom')
        print('Looking at Genus')
        for commonName, latinName in TAXONOMY_DAL.generate_default_genus_entries():
            obj, created = Genus.objects.get_or_create(kingdom=plantKingdom, name=commonName, latin_name=latinName)
            if created:
                print('Created Genus "{0}"'.format(latinName))
        print('Done.')
