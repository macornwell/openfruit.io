from django_geo_db.models import Location


class GeographyDAL:

    def get_unique_location_count(self):
        return Location.objects.count()


GEOGRAPHY_DAL = GeographyDAL()
