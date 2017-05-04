from django.contrib import admin
from openfruit.taxonomy.models import Kingdom, Genus, Species, Cultivar
from openfruit.taxonomy.forms import SpeciesForm, CultivarForm


class SpeciesAdmin(admin.ModelAdmin):
    form = SpeciesForm


class CultivarAdmin(admin.ModelAdmin):
    form = CultivarForm


admin.site.register(Kingdom)
admin.site.register(Genus)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Cultivar, CultivarAdmin)
