from rest_framework import serializers
from openfruit.reports.event.models import EventReport


class EventReportSerializer(serializers.ModelSerializer):
    event_type_text = serializers.SerializerMethodField()
    datetime = serializers.DateTimeField(format='%Y%m%d - %H:%M:%S')

    def get_event_type_text(self, obj):
        return str(obj.event_type.type)


    class Meta:
        model = EventReport
        fields = ('event_report_id', 'submitted_by', 'datetime', 'plant', 'event_type', 'event_type_text', 'notes')
