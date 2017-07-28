from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from openfruit.geography.models import Zipcode, Location


class Signup(models.Model):
    signup_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    zipcode = models.ForeignKey(Zipcode)
    new_location_lat_lon = models.CharField(max_length=20, blank=True, null=True)
    new_location_name = models.CharField(max_length=20, blank=True, null=True)
    existing_location = models.ForeignKey(Location, blank=True, null=True)
    organization = models.CharField(max_length=50, blank=True, null=True, help_text="If you belong to an organization such as a University, Business or Non-Profit, place it here.")
    request_to_be_a_curator = models.BooleanField(help_text="If you would like to become a curator.", default=False)
    reason_to_be_curator = models.TextField(help_text="A brief explination of why you should be considered for becoming a curator.", blank=True, null=True)


class UserProfile(models.Model):
    user_profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    location = models.ForeignKey(Location)
    organization = models.CharField(max_length=50, blank=True, null=True, help_text="If you belong to an organization such as a University, Business or Non-Profit, place it here.")

    def __str__(self):
        return "{0}'s Profile".format(self.user.username)

