from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django import forms
from dal.autocomplete import ModelSelect2
from openfruit.userdata.models import Signup, UserProfile

class SignupForm(ModelForm):
    class Meta:
        model = Signup
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',
                  'zipcode',
                  'new_location_lat_lon',
                  'new_location_name',
                  'existing_location',
                  'organization',
                  'request_to_be_a_curator',
                  'reason_to_be_curator',
                  ]
        widgets = {
            'password': forms.PasswordInput(),
            'zipcode': ModelSelect2(url='zipcode-autocomplete'),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'location',
            'organization',
        ]
        widgets = {
            'location': ModelSelect2(url='named-location-autocomplete'),
        }
