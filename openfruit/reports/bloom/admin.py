from django.contrib import admin
from openfruit.reports.bloom.models import BloomReport
from openfruit.common.admin import FilterUserAdmin


class BloomReportAdmin(FilterUserAdmin):
    pass

admin.site.register(BloomReport, BloomReportAdmin)

