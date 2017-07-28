from django import forms
from dal.autocomplete import ModelSelect2
from datetimewidget.widgets import DateTimeWidget
from openfruit.reports.event.models import EventReport

class EventReportForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S',], widget=DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3))
    class Meta:
        model = EventReport
        widgets = {
            'plant': ModelSelect2(url='fruiting-plant-autocomplete'),
            'datetime': DateTimeWidget(attrs={'id': 'datetime-id'}, usel10n=True, bootstrap_version=3),
            }
        fields = (
            'submitted_by', 'datetime', 'plant', 'event_type', 'affinity', 'image', 'notes'
        )

