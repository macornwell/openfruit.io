from django.test import TestCase
from openfruit.taxonomy.management.commands import setup_default_taxonomy, populate_common_uses
from openfruit.taxonomy.models import Kingdom, Genus, Species, Cultivar


def populate_taxonomy_test_data():
    command = setup_default_taxonomy.Command()
    command.populate()
    command = populate_common_uses.Command()
    command.populate()
    malus = Genus.objects.get(latin_name='Malus')
    domestica = Species.objects.create(genus=malus, latin_name='Malus domestica')
    ben_davis = Cultivar.objects.create(species=domestica, name='Ben Davis')
