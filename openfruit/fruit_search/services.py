from django_geo_db import models as GeoModels
from openfruit.taxonomy.models import Cultivar, FruitUsageType
from openfruit.fruit_reference.models import FruitReference
from openfruit.reports.disease.models import DiseaseResistanceReport, DiseaseType



class FruitSearchService:

    def filter_multiple_queries(self, queries_list):
        queryset = None
        if not queries_list:
            return Cultivar.objects.all()
        for l in queries_list:
            inner_query = self.filter(
                l.get('species', None),
                l.get('states', []),
                l.get('uses', []),
                l.get('year_low', None),
                l.get('year_high', None),
                l.get('ripening_low', None),
                l.get('ripening_high', None),
                l.get('references', []),
                l.get('chromosomes', None),
                l.get('resistances', []),
            )
            if not queryset:
                queryset = inner_query
            else:
                queryset = queryset | inner_query
        if not queryset:
            return []
        distinct_keys = {}
        for obj in queryset:
            if obj.cultivar_id not in distinct_keys:
                distinct_keys[obj.cultivar_id] = obj
        return sorted(distinct_keys.values(), key=lambda x: x.name)


    def filter(self, species, states, use_list, year_low, year_high, ripening_low,
               ripening_high, references, chromosomes, resistances):
        results = Cultivar.objects.all()
        if species:
            results = results.filter(species__latin_name=species)
        if states:
            states = GeoModels.State.objects.filter(name__in=states).values_list('state_id', flat=True)
            results = results.filter(origin_location__state_id__in=states)
        if use_list:
            if 'Other' in use_list:
                results = results.filter(uses=None)
            else:
                uses = FruitUsageType.objects.filter(type__in=use_list)
                for use in uses:
                    results = results.filter(uses=use)
        if year_low:
            results = results.filter(origin_year__gte=year_low)
        if year_high:
            results = results.filter(origin_year__lte=year_high)
        if ripening_low:
            results = results.filter(ripens_early__gte=ripening_low)
        if ripening_high:
            results = results.filter(ripens_late__lte=ripening_high)
        if references:
            for r in references:
                cultivar_list = FruitReference.objects.get(pk=r).cultivar_list.values_list('cultivar_id')
                results = results.filter(cultivar_id__in=cultivar_list)
        if chromosomes:
            results = results.filter(chromosome_count=chromosomes)
        if resistances:
            resistances = DiseaseType.objects.filter(type__in=resistances)
            reports = DiseaseResistanceReport.objects.filter(resistance_level='e', disease_type__in=resistances)
            all_resistant_cultivars = []
            for r in reports:
                if r.cultivar not in all_resistant_cultivars:
                    all_resistant_cultivars.append(r.cultivar.cultivar_id)
            results = results.filter(cultivar_id__in=all_resistant_cultivars)

        results = results.order_by('name')
        return results

FRUIT_SEARCH_SERVICE = FruitSearchService()
