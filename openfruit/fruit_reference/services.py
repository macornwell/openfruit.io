from openfruit.fruit_reference.models import FruitReference


class FruitReferenceService:

    def get_book_references(self):
        return FruitReference.objects.filter(type__type='Book').order_by('title')

FRUIT_REFERENCE_SERVICE = FruitReferenceService()
