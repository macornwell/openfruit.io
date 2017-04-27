from django.forms.models import ModelForm
from openfruit.taxonomy.models import Species, Cultivar, Genus


class GenusForm(ModelForm):
    class Meta:
        model = Genus
        fields = ['kingdom',
                  'latin_name',
                  'name',
                  ]


class SpeciesForm(ModelForm):
    class Meta:
        model = Species
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
                  ]


