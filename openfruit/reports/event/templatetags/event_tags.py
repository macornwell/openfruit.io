from django import template

register = template.Library()

@register.assignment_tag
def should_display_form_field(field):
    filter = {'event_type', 'affinity', 'submitted_by'}
    if field.name in filter:
        return False
    return True

@register.assignment_tag
def is_image(field):
    if field.name == 'image':
        return True
    return False


