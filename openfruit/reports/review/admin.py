from django.contrib import admin
from openfruit.reports.review.models import FruitReviewReport
from openfruit.common.admin import FilterUserAdmin


class FruitReviewReportAdmin(FilterUserAdmin):
    pass

admin.site.register(FruitReviewReport, FruitReviewReportAdmin)
