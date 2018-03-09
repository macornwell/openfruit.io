from django import forms
from dal.autocomplete import ModelSelect2
from datetimewidget.widgets import DateTimeWidget
from openfruit.reports.review.models import FruitReview


class FruitReviewForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S',], widget=DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3))
    class Meta:
        model = FruitReview
        widgets = {
            'fruiting_plant': ModelSelect2(url='fruiting-plant-autocomplete'),
            'datetime': DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3),
            }
        fields = ('submitted_by', 'datetime', 'fruiting_plant', 'sweet',
            'sour', 'bitter', 'juicy', 'firm', 'was_picked_early',
            'rating', 'text'
        )

