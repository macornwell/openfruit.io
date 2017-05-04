from django.contrib.auth.models import User
from django.db.models.signals import post_save


def update_user_location(sender, instance, **kwargs):
    instance.profile.save()

