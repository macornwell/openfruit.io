from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput
from django import forms
from django.urls import reverse

from dal.autocomplete import ModelSelect2
from datetimewidget.widgets import DateWidget
from openfruit.taxonomy.models import Species, Cultivar, Genus, FruitingPlant
from openfruit.common.widgets import CustomRelatedFieldWidgetWrapper
from django_geo_db.models import Location

class FruitingPlantForm(ModelForm):
    class Meta:
        model = FruitingPlant
        fields = [
            'fruiting_plant_id',
            'created_by',
            'species',
            'cultivar',
            'location',
            'geocoordinate',
            'date_planted',
            'date_died',
        ]
        widgets = {
            'fruiting_plant_id': HiddenInput(),
            'species': ModelSelect2(url='species-autocomplete'),
            'cultivar': ModelSelect2(url='cultivar-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            'location': ModelSelect2(url='named-location-autocomplete'),
            'created_by': ModelSelect2(url='curator-only-user-autocomplete'),
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
        self.fields['location'].widget = CustomRelatedFieldWidgetWrapper(
            ModelSelect2(url='location-autocomplete'),
            reverse('admin:django_geo_db_location_add') + "?_to_field=location_id&_popup=1",
            True)
        self.fields['location'].queryset = Location.objects.all()

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
            'created_by',
            'species',
            'cultivar',
            'location',
            'date_planted',
        ]
        widgets = {
            'created_by': HiddenInput(),
            'species': ModelSelect2(url='species-autocomplete'),
            'cultivar': ModelSelect2(url='cultivar-autocomplete'),
            'location': ModelSelect2(url='location-autocomplete'),
            'date_planted': DateWidget(usel10n=True, bootstrap_version=3),
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

