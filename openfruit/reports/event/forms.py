from django import forms
from dal.autocomplete import ModelSelect2
from datetimewidget.widgets import DateTimeWidget
from openfruit.reports.event.models import EventReport

class EventReportForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S',], widget=DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3))
    class Meta:
        model = EventReport
        widgets = {
            'location': ModelSelect2(url='named-location-autocomplete'),
            'cultivar': ModelSelect2(url='cultivar-autocomplete'),
            'species': ModelSelect2(url='species-autocomplete'),
            'datetime': DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3),
            }
        fields = (
            'submitted_by', 'datetime', 'location', 'species', 'cultivar', 'event_type', 'affinity', 'image', 'notes'
        )

