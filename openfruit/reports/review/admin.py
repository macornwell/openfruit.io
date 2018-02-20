from django.contrib import admin
from openfruit.reports.review.models import FruitReview, FruitReviewImage
from openfruit.common.admin import FilterUserAdmin


class FruitReviewAdmin(FilterUserAdmin):
    pass

admin.site.register(FruitReview, FruitReviewAdmin)
admin.site.register(FruitReviewImage)
