from django.contrib import admin
from openfruit.geography.models import Location, City, Continent, Country, State

admin.site.register(Location)
admin.site.register(City)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
