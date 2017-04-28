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
        login_url = reverse('admin:login')
    except NoReverseMatch:
        return ''

    snippet = """
              <li><a class="btn btn-lg" href='{href}?next={next}'>Log in</a></li>
              """
    snippet = format_html(snippet, href=login_url, next=escape(request.path))

    return mark_safe(snippet)

@register.simple_tag
def openfruit_logout(request, user):
    try:
        logout_url = reverse('admin:logout')
    except NoReverseMatch:
        snippet = format_html('<li class="btn btn-lg btn-primary">{user}</li>', user=escape(user))
        return mark_safe(snippet)
    snippet = """<li role="presentation" class="dropdown">
                            <a class="dropdown-toggle btn btn-lg" data-toggle="dropdown"
                               role="button"
                               aria-expanded="false">
                               {user}
                                <b class="caret"></b>
                            </a>
                            <ul class="dropdown-menu nav-submenu" role="menu">
                                <li role="menu">
                                    <a class="btn btn-lg" href="/admin">Advanced</a>
                                </li>
                                <li role="presentation">
                                    <a class="btn btn-lg" href='settings'>Settings</a></li>
                                </li>
                                <li role="presentation">
                                    <a class="btn btn-lg" href='{href}?next={next}'>Log out</a></li>
                                </li>
                            </ul>
                        </li>"""
    snippet = format_html(snippet, user=escape(user), href=logout_url, next=escape(request.path))

    return mark_safe(snippet)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

