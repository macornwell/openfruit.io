from django.contrib import admin

from openfruit.geography.models import Location, City, Continent, Country, \
    State, GeoCoordinate, UserGeographySettings, UserLocation
from openfruit.geography.forms import UserLocationForm, LocationForm, CityForm, UserGeographySettingsForm


class UserLocationAdmin(admin.ModelAdmin):
    form = UserLocationForm

class LocationAdmin(admin.ModelAdmin):
    form = LocationForm

class CityAdmin(admin.ModelAdmin):
    form = CityForm

class UserGeographySettingsAdmin(admin.ModelAdmin):
    form = UserGeographySettingsForm



admin.site.register(City, CityAdmin)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(GeoCoordinate)
admin.site.register(UserGeographySettings, UserGeographySettingsAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(Location, LocationAdmin)


