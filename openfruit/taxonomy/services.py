import os
import csv
from openfruit.settings import BASE_DIR
from openfruit.taxonomy.models import Species, Genus


def generate_default_genus_entries():
    """
    Returns a list of (common name, latin name)
    :return:
    """
    with open(os.path.join(BASE_DIR, 'openfruit', 'taxonomy', 'default_genus.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            commonName = row['common_name'].strip()
            latinName = row['latin_name'].strip()
            yield (commonName, latinName)


def get_genus_to_species_count():
    """
    Gets a dictionary of genus primary keys to the number of species that have that genus.
    If a genus has no species associated with it, it will be in the dictionary as a 0.
    :return:
    """
    tupleList = Species.objects.filter(genus_id__isnull=False).values_list('genus_id', 'species_id')
    dict = {}
    for genusID, speciesID in tupleList:
        if genusID not in dict:
            dict[genusID] = 0
        dict[genusID] += 1
    idList = Genus.objects.all().values_list('genus_id')
    for tuple in idList:
        id = tuple[0]
        if id not in dict:
            dict[id] = 0
    return dict