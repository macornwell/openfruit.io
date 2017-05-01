from dal import autocomplete
from django.db.models import Q
from openfruit.geography.models import Location, City, Zipcode, GeoCoordinate


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        qs = Location.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q) |
                Q(generated_name__endswith=self.q)
            )
        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q) |
                Q(generated_name__endswith=self.q)
            )
        return qs


class ZipcodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Zipcode.objects.none()

        qs = Zipcode.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q)
            )
        return qs


class GeoCoordinateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return GeoCoordinate.objects.none()

        qs = GeoCoordinate.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q)
            )
        return qs