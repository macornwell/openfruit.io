from django.contrib import admin
from openfruit.taxonomy.models import Kingdom, Genus, Species, Cultivar, FruitingPlant, FruitUsageType, GenusImage, SpeciesImage
from openfruit.taxonomy.forms import SpeciesForm, CultivarForm, FruitingPlantForm


class SpeciesAdmin(admin.ModelAdmin):
    form = SpeciesForm

class CultivarAdmin(admin.ModelAdmin):
    form = CultivarForm

class FruitingPlantAdmin(admin.ModelAdmin):
    form = FruitingPlantForm


admin.site.register(Kingdom)
admin.site.register(Genus)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Cultivar, CultivarAdmin)
admin.site.register(FruitingPlant, FruitingPlantAdmin)
admin.site.register(FruitUsageType)
admin.site.register(GenusImage)
admin.site.register(SpeciesImage)
