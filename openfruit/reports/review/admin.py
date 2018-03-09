from django.contrib import admin
from openfruit.common.admin import FilterUserAdmin
from openfruit.reports.review.models import FruitReview, FruitReviewImage
from openfruit.reports.review.forms import FruitReviewForm


class FruitReviewAdmin(FilterUserAdmin):
    form = FruitReviewForm
    pass


admin.site.register(FruitReview, FruitReviewAdmin)
admin.site.register(FruitReviewImage)
