from django.contrib.auth.models import Group
from openfruit.settings import get_user_models_for_permissions

CURATOR_GROUP_NAME = 'Curator'
USER_GROUP_NAME = 'User'

def is_curator(user):
    try:
        obj = Group.objects.get(name=CURATOR_GROUP_NAME) in user.groups.all() or user.is_superuser
    except:
        raise Exception('Curator group has not been initialized.')
    return obj


def setup_user_permissions_and_groups(user):
    user.is_staff = True
    user.groups.add(Group.objects.get(name=USER_GROUP_NAME))


