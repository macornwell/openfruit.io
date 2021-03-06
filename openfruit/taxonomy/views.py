import json
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, Http404, HttpResponseRedirect, HttpResponse, reverse, get_object_or_404, redirect
from django.http import HttpResponseServerError
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from openfruit.common.views import NameAutocomplete, GeneratedNameAutocomplete, BaseAutocompleteQuerysetView
from django_geo_db.models import GeoCoordinate
from django_geo_db.utilities import get_lat_lon_from_string
from openfruit.taxonomy.forms import SpeciesForm, GenusForm, FruitingPlantQuickForm
from openfruit.taxonomy.models import Species, Cultivar, Genus, Kingdom, FruitingPlant, \
    FruitUsageType, RIPENING_MONTH_CHOICES, CHROMOSOME_CHOICES
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.userdata.services import USER_DATA_DAL
from openfruit.reports.event.services import EVENT_DAL


class TaxonomyRestAPIMixin:

    def get_species_and_cultivar(self, request):
        species = request.query_params.get('species', None)
        if not species:
            raise ParseError('Error: species')
        cultivar = request.query_params.get('cultivar', None)
        if not cultivar:
            raise ParseError('Error: cultivar')
        return species, cultivar


@permission_classes((IsAuthenticated,))
def search(request):
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    data = {
        'token': token,
    }
    return render(request, template_name='taxonomy/search.html', context=data)


class KingdomListView(ListView):
    model = Kingdom
    template_name = 'taxonomy/kingdom-list.html'


class GenusListView(ListView):
    model = Genus
    template_name = 'taxonomy/genus-list.html'
    queryset = Genus.objects.all()

    def get_context_data(self, **kwargs):
        kingdom = self.kwargs['kingdom']
        kingdom = Kingdom.objects.filter(latin_name__iexact=kingdom).first()
        context = super(GenusListView, self).get_context_data(**kwargs)
        context['kingdom'] = kingdom
        context['genus_to_species_count'] = TAXONOMY_DAL.get_genus_to_species_count()
        return context


class SpeciesListView(ListView):
    model = Species
    template_name = 'taxonomy/species-list.html'


class CultivarListView(ListView):
    model = Cultivar
    template_name = 'taxonomy/cultivar-list.html'


class GenusDetailView(DetailView):
    model = Genus
    template_name = 'taxonomy/genus-detail.html'

    def get(self, request, kingdom=None, genus=None, *args, **kwargs):
        kingdom = Kingdom.objects.get_kingdom_by_name(kingdom)
        if not kingdom:
            raise Http404(request)
        genus = Genus.objects.get_genus_by_name(genus)
        if not genus:
            raise Http404(request)
        speciesList = Species.objects.get_species_from_genus(genus)
        data = {
            'kingdom': kingdom,
            'genus': genus,
            'species_list': speciesList,
        }
        return render(request, self.template_name, data)


class SpeciesDetailView(DetailView):
    model = Species
    template_name = 'taxonomy/species-detail.html'

    def get(self, request, kingdom=None, genus=None, species=None, *args, **kwargs):
        kingdom = Kingdom.objects.get_kingdom_by_name(kingdom)
        if not kingdom:
            raise Http404(request)
        genus = Genus.objects.get_genus_by_name(genus)
        if not genus:
            raise Http404(request)
        species = Species.objects.get_species_by_name(species)
        if not species:
            raise Http404(request)
        cultivars = Cultivar.objects.get_cultivars_from_species(species)
        data = {
            'kingdom': kingdom,
            'genus': genus,
            'species': species,
            'cultivar_list': cultivars,
        }
        return render(request, self.template_name, data)


class CultivarDetailView(DetailView):
    model = Cultivar
    template_name = 'taxonomy/cultivar-detail.html'

    def get(self, request, kingdom=None, genus=None, species=None, cultivar=None, *args, **kwargs):
        kingdom = Kingdom.objects.get_kingdom_by_name(kingdom)
        if not kingdom:
            raise Http404(request)
        genus = Genus.objects.get_genus_by_name(genus)
        if not genus:
            raise Http404(request)
        species = Species.objects.get_species_by_name(species)
        if not species:
            raise Http404(request)
        cultivar = Cultivar.objects.get_cultivar_by_name(species, cultivar)
        if not cultivar:
            raise Http404(request)
        data = {
            'kingdom': kingdom,
            'genus': genus,
            'species': species,
            'cultivar': cultivar,
        }
        return render(request, self.template_name, data)


def cultivar_detail_view_redirect(request, cultivar_id):
    cultivar = TAXONOMY_DAL.get_cultivar_by_id(cultivar_id)
    species = cultivar.species
    genus = species.genus
    kingdom = genus.kingdom
    return redirect('browse-cultivar-detail', kingdom.name, genus.name, species.name, cultivar.name)


def species_detail_view_redirect(request, species_id):
    species = TAXONOMY_DAL.get_species_by_id(species_id)
    genus = species.genus
    kingdom = genus.kingdom
    return redirect('browse-species-detail', kingdom.name, genus.name, species.name)


class GenusFormView(View):
    form_class = GenusForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/genus.html'

    @method_decorator(login_required)
    def get(self, request, id=None, *args, **kwargs):
        genus = None
        if id:
            genus = get_object_or_404(Genus, pk=id)
        form = self.form_class(initial=self.initial, instance=genus)
        data = self.__get_data(form, genus is None)
        return render(request, self.template_name, data)

    @method_decorator(login_required)
    def post(self, request, id=None, *args, **kwargs):
        data = request.POST.copy()
        genus = None
        if id:
            genus = get_object_or_404(Genus, pk=id)
            form = self.form_class(request.POST, request.FILES, instance=genus)
        else:
            form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            success = False
            try:
                instance = form.save(commit=False)
                if genus:
                    if genus.featured_image:
                        instance.featured_image = genus.featured_image
                    if 'featured_image' in form.cleaned_data and form.cleaned_data['featured_image']:
                        instance.featured_image = form.cleaned_data['featured_image']
                    if 'image-clear' in data:
                        instance.featured_image = None
                instance.save()
                success = True
            except Exception as e:
                form.add_error(None, 'Error occurred that prevent this from saving.')
            if success:
                if 'add-new' in data:
                    return HttpResponseRedirect(reverse('genus'))
                return HttpResponseRedirect(reverse('genus', kwargs={'id':instance.genus_id}))
            pass
        data = self.__get_data(form, isAdd=genus is None)
        return render(request, self.template_name, data)

    def __get_data(self, form, isAdd=False):
        data = {
            'form': form,
            'is_add': isAdd,
        }
        return data


class SpeciesFormView(View):
    form_class = SpeciesForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/species.html'

    @method_decorator(login_required)
    def get(self, request, genusID, id=None, *args, **kwargs):
        species = None
        genus = Genus.objects.get(pk=genusID)
        if id:
            species = get_object_or_404(Species, pk=id)
        initial = self.initial.copy()
        initial['genus'] = genus
        form = self.form_class(initial=initial, instance=species)
        data = self.__get_data(species, genusID, form, species is None)
        return render(request, self.template_name, data)

    @method_decorator(login_required)
    def post(self, request, genusID, id=None, *args, **kwargs):
        data = request.POST.copy()
        species = None
        if id:
            species = get_object_or_404(Species, pk=id)
            form = self.form_class(request.POST, request.FILES, instance=species)
        else:
            form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            success = False
            instance = None
            try:
                instance = form.save(commit=False)
                if species:
                    if species.featured_image:
                        instance.featured_image = species.featured_image
                    if 'featured_image' in form.cleaned_data and form.cleaned_data['featured_image']:
                        instance.featured_image = form.cleaned_data['featured_image']
                    if 'image-clear' in data:
                        instance.featured_image = None
                instance.save()
                success = True
            except Exception as e:
                form.add_error(None, 'Error occurred that prevent this from saving.')
            if success:
                if 'add-new' in data:
                    return HttpResponseRedirect(reverse('species', kwargs={'genusID': genusID}))
                return HttpResponseRedirect(reverse('species', kwargs={'id': instance.species_id, 'genusID': genusID}))
            pass
        data = self.__get_data(species, genusID, form, isAdd=species is None)
        return render(request, self.template_name, data)

    def __get_data(self, species, genusID, form, isAdd=False):
        genus = None
        if species:
            genus = species.genus
            kingdom = genus.kingdom
        else:
            genus = Genus.objects.get(pk=genusID)
            kingdom = Kingdom.objects.filter(latin_name__iexact='Plantae').first()
        data = {
            'form': form,
            'is_add': isAdd,
            'kingdom': kingdom,
            'genus': genus
        }
        return data


class CultivarFormView(View):
    initial = {'key': 'value'}
    template_name = 'taxonomy/cultivar-detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass


class FruitingPlantFormView(View):
    form_class = FruitingPlantQuickForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/fruiting_plant_form.html'

    def __get_data(self, form, requestDict):
        if 'lat' in requestDict and 'lon' in requestDict:
            centerLat = requestDict['lat']
            centerLon = requestDict['lon']
        elif form.instance:
            centerLat = str(form.instance.geocoordinate.lat)
            centerLon = str(form.instance.geocoordinate.lon)

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
        profile = USER_DATA_DAL.get_user_profile(request.user)
        fruitingPlant = None
        if 'id' in kwargs and kwargs['id']:
            fruitingPlant = TAXONOMY_DAL.get_fruiting_plant_by_id(kwargs['id'])
            form = FruitingPlantQuickForm(instance=fruitingPlant)
        else:
            form = FruitingPlantQuickForm(initial={'created_by':request.user, 'location': profile.location})
        centerLat = settings.GM_SETTINGS.lat
        centerLon = settings.GM_SETTINGS.lon
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
        postData['created_by'] = request.user.id

        form = FruitingPlantQuickForm(postData)
        data = self.__get_data(form, request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            if 'id' in kwargs and kwargs['id']:
                model.fruiting_plant_id = kwargs['id']
            model.geocoordinate = coordinate
            model.save()
            return redirect(nextUrl)
        return render(request, self.template_name, data)


class FruitingPlantDetailsView(View):
    initial = {'key': 'value'}
    template_name = 'taxonomy/fruiting_plant_details.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        fruiting_plant = TAXONOMY_DAL.get_fruiting_plant_by_id(id)
        all_events = EVENT_DAL.get_all_events_for_fruiting_plant(fruiting_plant)
        leafs = EVENT_DAL.get_aggregate_event_summary_for_the_year(all_events, 'Leafing Out')
        blooms = EVENT_DAL.get_aggregate_event_summary_for_the_year(all_events, 'Blooming')
        ripenings = EVENT_DAL.get_aggregate_event_summary_for_the_year(all_events, 'Ripening')
        data = {
            'model': fruiting_plant,
            'leafs': leafs,
            'blooms': blooms,
            'ripenings': ripenings,
            'all_events': all_events,
        }
        return render(request, self.template_name, data)



################
# JSON Ajax
################
def move_fruiting_plant(request):
    if request.method == 'POST':
        jsonData = json.loads(request.read().decode('utf-8'))
        try:
            fruitingPlantID = jsonData['fruiting_plant_id']
            coordinateString = jsonData['coordinate']
        except KeyError:
            return HttpResponseServerError("Malformed data!")
        lat,lon = get_lat_lon_from_string(coordinateString)
        fruitingPlant = TAXONOMY_DAL.move_fruiting_plant(fruitingPlantID, lat, lon)
    return HttpResponse("OK")



################
# Auto Completes
################

class FruitingPlantAutocomplete(BaseAutocompleteQuerysetView):
    model_type = FruitingPlant

    def filter(self, qs):
        qs = qs.filter(submitted_by=self.request.user)
        qs = qs.filter(Q(cultivar__generated_name__startswith=self.q) |
                       Q(species__generated_name__startswith=self.q)
        )
        return qs

class GenusAutocomplete(GeneratedNameAutocomplete):
    model_type = Genus
    is_contains = True


class SpeciesAutocomplete(GeneratedNameAutocomplete):
    model_type = Species
    is_contains = True


class CultivarAutocomplete(NameAutocomplete):
    model_type = Cultivar
    is_contains = True

