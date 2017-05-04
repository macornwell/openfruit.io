from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.utils.decorators import method_decorator
from openfruit.reports.event.models import EventReport
from openfruit.reports.event.forms import EventReportForm
from openfruit.reports.event.services import EVENT_DAL
from openfruit.geography.services import GEO_DAL


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
                    instance.image = form.cleaned_data['image'] or None
                    instance.save()
                    success = True
                except Exception as e:
                    form.add_error(None, 'Error occurred that prevent this from saving.')
                if success:
                    if 'add-new' in data:
                        return HttpResponseRedirect(reverse(self.url_name))
                    return HttpResponseRedirect(reverse('home'))
        data = self.__get_data(form, request.user)
        return render(request, self.template_name, data)

