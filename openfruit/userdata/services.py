from openfruit.userdata.models import UserProfile


class UserDataDAL:

    def get_user_profile(self, user):
        return UserProfile.objects.filter(user=user).first()

USER_DATA_DAL = UserDataDAL()
