from django.db.models import Q
from dal import autocomplete
from openfruit.geography.models import Location, City, Zipcode, GeoCoordinate, UserLocation
from openfruit.geography.services import GEO_DAL


class UsersLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        user = self.request.user
        qs = UserLocation.objects.filter(user=user)

        if self.q:
            qs = qs.filter(
                Q(location__generated_name__icontains=self.q),
            )
        return qs

class NamedLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        qs = Location.objects.filter(name__isnull=False)

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q)
            )
        return qs

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
                Q(generated_name__iendswith=self.q)
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