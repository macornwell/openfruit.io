from openfruit.taxonomy.models import Cultivar, FruitUsageType
from openfruit.fruit_reference.models import FruitReference

class FruitSearchService:

    def filter(self, **kwargs):
        """
        species
        state
        use_list
        year_low
        year_high
        ripening_low
        ripening_high
        reference_id
        :param query_params:
        :return:
        """
        results = Cultivar.objects.all()
        if 'species' in kwargs:
            results.filter(species=kwargs['species'])
        if 'state' in kwargs:
            results.filter(origin_location__state__name=kwargs['state'])
        if 'use_list' in kwargs:
            uses = FruitUsageType.objects.filter(type__in=kwargs['use_list'])
            results = results.filter(use__in=uses)
        if 'year_low' in kwargs:
            results = results.filter(origin_year__gte=kwargs['year_low'])
        if 'year_high' in kwargs:
            results = results.filter(origin_year__lte=kwargs['year_high'])
        if 'ripening_low' in kwargs:
            results = results.filter(ripens_early=None)
        if 'ripening_high' in kwargs:
            results = results.filter(ripens_late=None)
        if 'reference_id' in kwargs:
            cultivar_list = FruitReference.objects.get(pk=kwargs['reference_id']).cultivar_list.values_list('cultivar_id')
            results = results.filter(cultivar_id__in=cultivar_list)
        return results

FRUIT_SEARCH_SERVICE = FruitSearchService()
