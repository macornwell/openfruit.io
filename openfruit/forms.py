from django.forms.models import ModelForm
from django import forms
from openfruit.common.models import User, Signup

class SignupForm(ModelForm):
    class Meta:
        model = Signup
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email',
                  'zipcode',
                  'organization',
                  'request_to_be_a_curator',
                  'reason_to_be_curator',
                  ]
        widgets = {
            'password': forms.PasswordInput(),
        }
