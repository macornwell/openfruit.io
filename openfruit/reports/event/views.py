import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse
from django.http import HttpResponseServerError
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils import timezone
from django.utils.decorators import method_decorator

from rest_framework import generics

from openfruit.reports.event.models import EventReport, DIED_TYPE
from openfruit.reports.event.forms import EventReportForm
from openfruit.reports.event.services import EVENT_DAL
from openfruit.reports.event.serializers import EventReportSerializer
from openfruit.taxonomy.services import TAXONOMY_DAL
from django_geo_db.services import GEO_DAL


class DistinctEventView(View):
    event_type = None
    url_name = None
    affinity = 0
    form_class = EventReportForm
    initial = {'key': 'value'}
    template_name = 'reports/event/add-event.html'

    def __get_data(self, form, user, isAdd=False):
        data = {
            'form': form,
            'event_type_readable': self.event_type,
            'event_type': EVENT_DAL.get_event_type_by_type(self.event_type),
            'is_add': isAdd,
            'url_name': self.url_name,
            'events': EVENT_DAL.get_last_events_by_user_and_type(user, self.event_type, 10)
        }
        return data

    @method_decorator(login_required)
    def get(self, request, id=None, *args, **kwargs):
        event = None
        isAdd = True
        if id:
            user = request.user
            event = EVENT_DAL.get_event_by_id(id)
            isAdd = False
            if not user.is_superuser:
                if event.submitted_by != user:
                    raise Http404()
        if not id and not event:
            settings = GEO_DAL.get_users_geography_settings(request.user)
            event = EventReport()
            event.location = settings.location
        form = self.form_class(instance=event)
        data = self.__get_data(form, request.user, isAdd)
        return render(request, self.template_name, data)

    @method_decorator(login_required)
    def post(self, request, id=None, *args, **kwargs):
        data = request.POST.copy()
        data.update({'submitted_by': request.user.id})
        data.update({'event_type': EVENT_DAL.get_event_type_by_type(self.event_type).event_type_id})
        data.update({'affinity': self.affinity})
        form = self.form_class(data, request.FILES)
        if form.is_valid():
            if not form.cleaned_data['cultivar'] and not form.cleaned_data['species']:
                form.add_error('cultivar', 'Must select either a species or a cultivar.')
                form.add_error('species', 'Must select either a species or a cultivar.')
            else:
                success = False
                try:
                    instance = form.save(commit=False)
                    if id:
                        instance.event_report_id = id
                        oldInstance = EVENT_DAL.get_event_by_id(id)
                        if oldInstance.image:
                            instance.image = oldInstance.image
                    if 'image' in form.cleaned_data and form.cleaned_data['image']:
                        instance.image = form.cleaned_data['image']
                    if 'image-clear' in data:
                        instance.image = None
                    instance.save()
                    success = True
                except Exception as e:
                    form.add_error(None, 'Error occurred that prevent this from saving.')
                if success:
                    if 'add-new' in data:
                        return HttpResponseRedirect(reverse(self.url_name))
                    return HttpResponseRedirect(reverse(self.url_name, kwargs={'id':id}))
        data = self.__get_data(form, request.user)
        return render(request, self.template_name, data)





################
# JSON
################

def add_event_record(request):
    if request.method == 'POST':
        jsonData = json.loads(request.read().decode('utf-8'))
        try:
            eventType = jsonData['event_type']
            fruitingPlantID = jsonData['fruiting_plant_id']
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        event = EVENT_DAL.get_event_type_by_type(eventType)
        fruitingPlant = TAXONOMY_DAL.get_fruiting_plant_by_id(fruitingPlantID)
        if event.type == DIED_TYPE:
            fruitingPlant.date_died = timezone.now()
            fruitingPlant.save()
        EVENT_DAL.create_event(request.user, event, fruitingPlant)
    return HttpResponse("OK")


class EventReportListView(generics.ListAPIView):
    serializer_class = EventReportSerializer

    def get_queryset(self):
        jsonData = self.request.GET
        try:
            fruitingPlantID = jsonData.get('fruiting_plant_id', None)
            submittedBy = jsonData.get('submitted_by', None)
            eventType = jsonData.get('event_type', None)
            types = jsonData.get('types', [])
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        events = EVENT_DAL.get_events(fruiting_plant_id=fruitingPlantID, submitted_by=submittedBy, event_type=eventType, types=types)
        return events



