from django.views.generic import View
from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework.generics import ListAPIView

from django_geo_db.models import GeoCoordinate
from django_geo_db.services import GEO_DAL
from django_geo_db.forms import LocationForm
from django_geo_db.serializers import StateSerializer

from openfruit.geography.services import GEOGRAPHY_DAL


class StateWithCultivarsListView(ListAPIView):
    queryset = GEOGRAPHY_DAL.get_states_with_fruits()
    serializer_class = StateSerializer


class LocationDetailView(View):
    form_class = LocationForm
    initial = {'key': 'value'}
    template_name = 'geography/location-details.html'

    def __get_data(self, form, requestDict):
        if 'lat' in requestDict and 'lon' in requestDict:
            centerLat = requestDict['lat']
            centerLon = requestDict['lon']
        elif form.instance:
            centerLat = str(form.instance.geocoordinate.lat)
            centerLon = str(form.instance.geocoordinate.lon)
        if not centerLat or not centerLon:
            raise Exception('Need location')

        data = {
            'form': form,
            'GM_SETTINGS': settings.GM_SETTINGS,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
            'center_lat': centerLat,
            'center_lon': centerLon,
            'zoom': 20,
        }
        return data

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        location = None
        if 'id' in kwargs and kwargs['id']:
            location = GEO_DAL.get_location_by_id(kwargs['id'])
            form = LocationForm(instance=location)
        else:
            form = LocationForm()
        data = self.__get_data(form, request.GET)
        return render(request, self.template_name, data)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        nextUrl = '/'
        if 'next' in request.GET:
            nextUrl = request.GET['next']
        postData = request.POST.copy()
        lat = postData['lat']
        lon = postData['lon']
        coordinate, created = GeoCoordinate.objects.get_or_create_by_lat_lon(lat, lon)

        form = LocationForm(postData)
        data = self.__get_data(form, request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            if 'id' in kwargs and kwargs['id']:
                model.location_id = kwargs['id']
            model.geocoordinate = coordinate
            model.save()
            return redirect(nextUrl)
        return render(request, self.template_name, data)
