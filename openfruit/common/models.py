from django.db import models
from django.contrib.auth.models import User

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Signup(models.Model):
    signup_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, blank=True, null=True)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    zipcode = IntegerRangeField(min_value=1, max_value=99999, help_text="Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.")
    organization = models.CharField(max_length=50, blank=True, null=True, help_text="If you belong to an organization such as a University, Business or Non-Profit, place it here.")
    request_to_be_a_curator = models.BooleanField(help_text="If you would like to become a curator.", default=False)
    reason_to_be_curator = models.TextField(help_text="A brief explination of why you should be considered for becoming a curator.", blank=True, null=True)


class UserProfile(models.Model):
    user_profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    zipcode = IntegerRangeField(min_value=1, max_value=99999, help_text="Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.")
    organization = models.CharField(max_length=50, blank=True, null=True, help_text="If you belong to an organization such as a University, Business or Non-Profit, place it here.")


