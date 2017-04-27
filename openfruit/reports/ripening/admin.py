from django.contrib import admin
from openfruit.reports.ripening.models import FruitRipeningReport
from openfruit.common.admin import FilterUserAdmin

class FruitRipeningReportAdmin(FilterUserAdmin):
    pass

admin.site.register(FruitRipeningReport, FruitRipeningReportAdmin)
