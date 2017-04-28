from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from openfruit.settings import get_curator_models, get_user_models_for_permissions
from openfruit.common.services import CURATOR_GROUP_NAME, USER_GROUP_NAME


class Command(BaseCommand):
    help = "Setups all default groups and permissions."

    def __add_full_permissions(self, model, obj):
        # Now what - Say I want to add 'Can add project' permission to new_group?
        permissions = Permission.objects.filter(codename__endswith=model.__name__.lower())
        for permission in permissions:
            obj.permissions.add(permission)


    def handle(self, *args, **options):
        data = (
            (CURATOR_GROUP_NAME, get_curator_models()),
            (USER_GROUP_NAME, get_user_models_for_permissions()),
        )
        for name, allowedModelTypes in data:
            try:
                obj = Group.objects.get(name=name)
            except Exception as e:
                obj = Group.objects.create(name=name)
                for model in allowedModelTypes:
                    ct = ContentType.objects.get_for_model(model)
                    self.__add_full_permissions(model, obj)
                obj.save()

