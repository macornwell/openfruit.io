import os
import csv
from openfruit.settings import BASE_DIR


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
