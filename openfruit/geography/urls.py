from openfruit.geography.views import LocationAutocomplete, ZipcodeAutocomplete, CityAutocomplete, GeoCoordinateAutocomplete
from django.conf.urls import url


urlpatterns = [
    url('^autocomplete/location/$',
        LocationAutocomplete.as_view(),
        name='location-autocomplete'),
    url('^autocomplete/zipcode/$',
        ZipcodeAutocomplete.as_view(),
        name='zipcode-autocomplete'),
    url('^autocomplete/city/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete'),
    url('^autocomplete/geocoordinate/$',
        GeoCoordinateAutocomplete.as_view(),
        name='geocoordinate-autocomplete'),
]
