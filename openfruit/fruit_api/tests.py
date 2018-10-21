from django.test import TestCase
from openfruit.fruit_api.services import FRUIT_API_SERVICE
from openfruit.taxonomy.models import Kingdom, Genus, Cultivar
from openfruit.taxonomy.tests import populate_taxonomy_test_data

FULL_SEARCH = {
    'addons': ['location', 'review', 'resistances'],
    'review_types': ['sweet', 'sour', 'firm', 'bitter', 'juicy', 'rating'],
    'review_metrics': ['avg', 'max', 'min']
}


class TestFruitAPIService(TestCase):
    def setUp(self):
        populate_taxonomy_test_data()
        self.not_there = FRUIT_API_SERVICE.full_cultivar_query('Malus domestica',
                                                               'Doesnt Exist',
                                                               addons=FULL_SEARCH['addons'],
                                                               review_types=FULL_SEARCH['review_types'],
                                                               review_metrics=FULL_SEARCH['review_metrics']
                                                               )
        print(Cultivar.objects.get(name='Ben Davis'))
        self.ben_davis = FRUIT_API_SERVICE.full_cultivar_query('Malus domestica',
                                                               'Ben Davis')

    def test_full_cultivar_query_with_is_not_there(self):
        self.assertIsNone(self.not_there)

    def test_full_cultivar_query_with_ben_davis_obj_is_dict(self):
        self.assertIsInstance(self.ben_davis, type(dict))


