from django_geo_db.models import Location, State
from openfruit.taxonomy.models import Cultivar


class GeographyDAL:

    def get_unique_location_count(self):
        return Location.objects.count()

    def get_states_with_fruits(self):
        state_list = Cultivar.objects.filter(origin_location__state__isnull=False).order_by('origin_location').values('origin_location__state_id').distinct()
        states = State.objects.filter(state_id__in=state_list)
        return states



GEOGRAPHY_DAL = GeographyDAL()
