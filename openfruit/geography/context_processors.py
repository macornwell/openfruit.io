from django.conf import settings
from openfruit.geography.services import GEO_DAL


def google_maps_api_key(request):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}


def google_maps_settings(request):
    return {'GM_SETTINGS': settings.GM_SETTINGS}


def user_map_settings(request):
    settings = None
    if request.user.is_authenticated():
        settings = GEO_DAL.get_users_geography_settings(request.user)
    return {'USER_GEO': settings}
