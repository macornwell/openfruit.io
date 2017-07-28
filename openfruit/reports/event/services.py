from openfruit.reports.event.models import EventType, EventReport

class EventDAL:

    def get_event_type_by_type(self, type):
        return EventType.objects.get(type=type)

    def get_event_by_id(self, id):
        return EventReport.objects.get(pk=id)

    def get_last_events_by_user_and_type(self, user, typeString, count):
        result = EventReport.objects.filter(submitted_by=user, event_type__type=typeString).order_by('-datetime')[:10]
        return result

    def create_event(self, user, eventType, fruitingPlant, notes=None, image=None):
        event = EventReport(submitted_by=user, plant=fruitingPlant, event_type=eventType, notes=None, image=None)
        event.save()
        return event

    def get_events(self, pk=None, fruiting_plant_id=None, submitted_by=None, event_type=None, types=[]):
        objects = EventReport.objects.all()
        if pk:
            objects = objects.filter(pk=pk)
        if fruiting_plant_id:
            objects = objects.filter(plant=fruiting_plant_id)
        if submitted_by:
            objects = objects.filter(submitted_by=submitted_by)
        if event_type:
            objects = objects.filter(event_type=event_type)
        if types:
            objects = objects.filter(event_type__type__in=types)
        objects = objects.order_by('-datetime')
        return objects



EVENT_DAL = EventDAL()
