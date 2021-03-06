from django import template
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def openfruit_login(request):
    """
    Include a login snippet if REST framework's login view is in the URLconf.
    """
    try:
        login_url = reverse('rest_framework:login')
    except NoReverseMatch:
        return ''

    snippet = """
              <li><a class="btn btn-lg btn-default nav-btn" href='{href}?next={next}'><i class="fa fa-sign-in" aria-hidden="true"></i></a></li>
              """
    snippet = format_html(snippet, href=login_url, next=escape(request.path))

    return mark_safe(snippet)

@register.simple_tag
def openfruit_logout(request, user):
    try:
        logout_url = reverse('rest_framework:logout')
    except NoReverseMatch:
        snippet = format_html('<li class="btn btn-lg btn-primary">{user}</li>', user=escape(user))
        return mark_safe(snippet)
    snippet = """
              <li role="presentation">
                <a class="btn btn-lg btn-default nav-btn" href='{href}?next={next}'><i class="fa fa-sign-out" aria-hidden="true"></i></a></li>
              </li>
              """
    snippet = format_html(snippet, user=escape(user), href=logout_url, next=escape(request.path))

    return mark_safe(snippet)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_even(list_of_items):
    if len(list_of_items) % 2 == 0:
        return True
    return False


@register.filter
def create_tuple_pairs(list_of_items):
    data = list(list_of_items)
    length = len(data)
    if length == 1:
        return [(data[0], None)]
    if length == 2:
        return [(data[0], data[1])]
    evens = data[::2]
    odds = data[1::2]
    results = []
    length = len(evens)
    for idx in range(length):
        obj = evens[idx]
        obj_2 = None
        if len(odds) > idx:
            obj_2 = odds[idx]
        results.append((obj, obj_2))
    return results


@register.inclusion_tag('common/multicheckbox.html')
def multi_checkbox(class_name, box_name, obj_list):
    return {'class_name': class_name,
            'box_name': box_name,
            'obj_list': obj_list
            }
