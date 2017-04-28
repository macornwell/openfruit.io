from django.contrib import admin
from openfruit.taxonomy.models import Kingdom, Genus, Species, Cultivar

admin.site.register(Kingdom)
admin.site.register(Genus)
admin.site.register(Species)
admin.site.register(Cultivar)
