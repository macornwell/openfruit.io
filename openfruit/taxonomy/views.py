from django.db.models import Q
from django.shortcuts import render, Http404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator

from openfruit.common.views import NameAutocomplete, GeneratedNameAutocomplete
from openfruit.taxonomy.forms import SpeciesForm, GenusForm
from openfruit.taxonomy.models import Species, Cultivar, Genus, Kingdom
from openfruit.taxonomy.services import GENUS_DAL


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
        context['genus_to_species_count'] = GENUS_DAL.get_genus_to_species_count()
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
        raise Exception('Not ready')


class GenusFormView(View):
    form_class = GenusForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/genus-form.html'

    @method_decorator(login_required)
    def get(self, request, genus=None, *args, **kwargs):
        if genus:
            genus = GENUS_DAL.get_genus_by_name(genus)
        form = self.form_class(initial=self.initial, instance=genus)
        return render(request, self.template_name, {'form': form, 'kingdom': kingdom})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

class SpeciesFormView(View):
    form_class = SpeciesForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/species-detail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)


class CultivarFormView(View):
    initial = {'key': 'value'}
    template_name = 'taxonomy/cultivar-detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass




################
# Auto Completes
################


class GenusAutocomplete(GeneratedNameAutocomplete):
    model_type = Genus
    is_contains = True


class SpeciesAutocomplete(GeneratedNameAutocomplete):
    model_type = Species
    is_contains = True


class CultivarAutocomplete(NameAutocomplete):
    model_type = Cultivar
