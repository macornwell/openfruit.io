from django_geo_db import models as GeoModels
from openfruit.taxonomy.models import Cultivar, FruitUsageType
from openfruit.fruit_reference.models import FruitReference
from openfruit.reports.disease.models import DiseaseResistanceReport, DiseaseType



class FruitSearchService:

    def filter(self, species, state, use_list, year_low, year_high, ripening_low,
               ripening_high, reference_id, chromosomes, resistances):
        results = Cultivar.objects.all()
        if species:
            results = results.filter(species__latin_name=species)
        if state:
            state = GeoModels.State.objects.get(name=state)
            results = results.filter(origin_location__state_id=state.state_id)
        if use_list:
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
        if reference_id:
            cultivar_list = FruitReference.objects.get(pk=reference_id).cultivar_list.values_list('cultivar_id')
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
