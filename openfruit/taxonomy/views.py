from django.shortcuts import render, Http404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import permission_required

from openfruit.taxonomy.forms import SpeciesForm, GenusForm
from openfruit.taxonomy.models import Species, Cultivar, Genus, Kingdom


class KingdomListView(ListView):
    model = Kingdom
    template_name = 'taxonomy/kingdom-list.html'


class GenusListView(ListView):
    model = Genus
    template_name = 'taxonomy/genus-list.html'

    def get_context_data(self, **kwargs):
        kingdom = self.kwargs['kingdom']
        kingdom = Kingdom.objects.filter(latin_name__iexact=kingdom).first()
        context = super(GenusListView, self).get_context_data(**kwargs)
        context['kingdom'] = kingdom
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
        kingdom = Kingdom.objects.filter(latin_name__iexact=kingdom).first()
        if not kingdom:
            raise Http404(request)
        genus = Genus.objects.filter(latin_name__iexact=genus).first()
        if not genus:
            raise Http404(request)
        data = {
            'kingdom': kingdom,
            'object': genus,
        }
        return render(request, self.template_name, data)




def display_genus(request, kingdom):
    kingdom = Kingdom.objects.filter(latin_name__iexact=kingdom).first()
    if not kingdom:
        raise Http404(request)
    return render(request, {'object'})

class GenusFormView(View):
    form_class = GenusForm
    initial = {'key': 'value'}
    template_name = 'taxonomy/genus-form.html'

    def get(self, request, kingdom=None, genus=None, *args, **kwargs):
        kingdom = Kingdom.objects.filter(latin_name__iexect=kingdom).first()
        if not kingdom:
            raise Http404(request)
        if genus:
            genus = Genus.objects.filter(kingdom=kingdom, latin_name__iexact=genus).first()
        if not request.user.is_staff:
            if not genus:
                raise Http404(request)
            return render(request, 'taxonomy/genus-detail.html', {'object': genus, 'kingdom': kingdom})
        form = self.form_class(initial=self.initial, instance=genus)
        return render(request, self.template_name, {'form': form, 'kingdom': kingdom})

    @permission_required('taxonomy.can add genus', login_url="/login/")
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
