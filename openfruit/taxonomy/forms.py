from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django import forms
from django.urls import reverse

from dal.autocomplete import ModelSelect2
from datetimewidget.widgets import DateWidget
from openfruit.taxonomy.models import Species, Cultivar, Genus, FruitingPlant
from openfruit.common.widgets import CustomRelatedFieldWidgetWrapper

class FruitingPlantForm(ModelForm):
    class Meta:
        model = FruitingPlant
        fields = [
            'user_manager',
            'species',
            'cultivar',
            'location',
            'geocoordinate',
            'planted',
            'is_private',
            'date_died',
        ]
        widgets = {
            'species': ModelSelect2(url='species-autocomplete'),
            'cultivar': ModelSelect2(url='cultivar-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            'location': ModelSelect2(url='named-location-autocomplete'),
            'user_manager': ModelSelect2(url='curator-only-user-autocomplete'),
        }

class FruitingPlantQuickForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FruitingPlantQuickForm,self).__init__(*args, **kwargs)
        self.fields['cultivar'].widget = CustomRelatedFieldWidgetWrapper(
                                                ModelSelect2(url='cultivar-autocomplete'),
                                                reverse('admin:taxonomy_cultivar_add') + "?_to_field=cultivar_id&_popup=1",
                                                True)
        self.fields['cultivar'].queryset = Cultivar.objects.all()
        self.fields['species'].widget = CustomRelatedFieldWidgetWrapper(
            ModelSelect2(url='species-autocomplete'),
            reverse('admin:taxonomy_species_add') + "?_to_field=species_id&_popup=1",
            True)
        self.fields['species'].queryset = Species.objects.all()

    class Media:
        ## media for the FilteredSelectMultiple widget
        css = {
            'all':('admin/' + 'css/widgets.css',),
        }
        # jsi18n is required by the widget
        js = ( 'admin/' + 'js/admin/RelatedObjectLookups.js',)

    class Meta:
        model = FruitingPlant
        fields = [
            'user_manager',
            'species',
            'cultivar',
            'location',
            'planted',
            'is_private'
        ]
        widgets = {
            'user_manager': HiddenInput(),
            'species': ModelSelect2(url='species-autocomplete'),
            'cultivar': ModelSelect2(url='cultivar-autocomplete'),
            'location': ModelSelect2(url='location-autocomplete'),
            'planted': DateWidget(usel10n=True, bootstrap_version=3),
        }



class GenusForm(ModelForm):
    class Meta:
        model = Genus
        fields = ['kingdom',
                  'latin_name',
                  'name',
                  'featured_image',
                  ]


class SpeciesForm(ModelForm):
    class Meta:
        model = Species
        widgets = {
            'origin': ModelSelect2(url='location-autocomplete'),
            'genus': ModelSelect2(url='genus-autocomplete'),
        }
        fields = ['genus',
                  'origin',
                  'latin_name',
                  'name',
                  'can_scale_with_pruning',
                  'years_till_full_size',
                  'full_size_height',
                  'full_size_width',
                  'years_till_first_production',
                  'years_till_full_production',
                  'featured_image',
                  'google_maps_image_url',
                  ]

    def clean(self):
        form_data = self.cleaned_data
        genus = form_data['genus']
        latinName = form_data['latin_name']
        if not latinName.startswith(genus.latin_name):
            self._errors['latin_name'] = ["Latin Name must start with species' latin name."]
            del form_data['latin_name']
        if latinName == genus.latin_name:
            self._errors['latin_name'] = ["Latin name must be different than the species' latin name."]
            del form_data['latin_name']
        return form_data


class CultivarForm(ModelForm):
    class Meta:
        model = Cultivar
        widgets = {
            'origin_location': ModelSelect2(url='location-autocomplete'),
            'species': ModelSelect2(url='species-autocomplete'),
            'parent_a': ModelSelect2(url='cultivar-autocomplete'),
            'parent_b': ModelSelect2(url='cultivar-autocomplete'),
        }
        fields = '__all__'

