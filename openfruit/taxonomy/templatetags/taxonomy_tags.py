from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_name_of_species_or_cultivar(species, cultivar):
    obj = species
    if cultivar:
        obj = cultivar
    return mark_safe(str(obj))

