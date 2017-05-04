from django.forms.models import ModelForm
from openfruit.taxonomy.models import Species, Cultivar, Genus
from dal.autocomplete import ModelSelect2

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
                  ]


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

