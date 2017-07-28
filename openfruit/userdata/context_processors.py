from openfruit.userdata.services import USER_DATA_DAL


def user_profile(request):
    profile = None
    if request.user.is_authenticated():
        profile = USER_DATA_DAL.get_user_profile(request.user)
    return {'USER_PROFILE': profile}
