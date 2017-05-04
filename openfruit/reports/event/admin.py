from django.contrib import admin
from openfruit.reports.event.models import EventReport
from openfruit.common.admin import FilterUserAdmin
from openfruit.reports.event.forms import EventReportForm

class EventReportAdmin(FilterUserAdmin):
    form = EventReportForm

admin.site.register(EventReport, EventReportAdmin)

