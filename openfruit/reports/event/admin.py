from django.contrib import admin
from openfruit.reports.event.models import EventReport
from openfruit.common.admin import FilterUserAdmin


class EventReportAdmin(FilterUserAdmin):
    pass

admin.site.register(EventReport, EventReportAdmin)

