from django.contrib import admin
from openfruit.reports.characteristics.models import FruitCharacteristicReport
from openfruit.common.admin import FilterUserAdmin


class FruitCharacteristicReportAdmin(FilterUserAdmin):
    pass

admin.site.register(FruitCharacteristicReport, FruitCharacteristicReportAdmin)
