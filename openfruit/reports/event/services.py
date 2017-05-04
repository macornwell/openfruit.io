from openfruit.reports.event.models import EventType, EventReport

class EventDAL:

    def get_event_type_by_type(self, type):
        return EventType.objects.get(type=type)

    def get_event_by_id(self, id):
        return EventReport.objects.get(pk=id)

    def get_last_events_by_user_and_type(self, user, typeString, count):
        result = EventReport.objects.filter(submitted_by=user, event_type__type=typeString).order_by('-datetime')[:10]
        return result

EVENT_DAL = EventDAL()
