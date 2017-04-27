from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib import messages
from openfruit.common.models import UserProfile
from openfruit.forms import SignupForm
from openfruit.common.services import setup_user_permissions_and_groups

def get_add_model_form(request, templatePath, modelType, modelTypeFriendlyName, datePropertyName, formType, customValidator=None, additionalDataGenerator=None):
    if request.method == 'POST':
        form = formType(request.POST)
        if form.is_valid():
            passedCustomValidation = True
            if customValidator:
                passedCustomValidation = customValidator(request, form)
                if not passedCustomValidation:
                    messages.error(request, '{0} failed validation.'.format(modelType.__name__))
            if passedCustomValidation:
                model = form.save(commit=False)
                model.user = request.user
                model.save()
                messages.info(request, '{0} Saved!'.format(modelType.__name__))
        else:
            messages.error(request, 'Unable to save {0}.'.format(modelType.__name__))
    else:
        form = formType()
    data = {
        'form': form,
        'add_model_type': modelTypeFriendlyName,
    }
    if additionalDataGenerator:
        for key, value in additionalDataGenerator():
            data[key] = value
    return render(request, templatePath, data)


def home(request):
    data = {}
    loginUrl = reverse('admin:login')
    loginNextUrl = escape(request.path)
    data['loginUrl'] = '{0}?next={1}'.format(loginUrl, loginNextUrl)
    return render(template_name='home.html', context=data, request=request)



class SignupFormView(View):
    form_class = SignupForm
    initial = {'key': 'value'}
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            signupModel = form.save(commit=False)
            valid = True
            try:
                user = User(username=signupModel.username,
                            first_name=signupModel.first_name,
                            last_name=signupModel.last_name,
                            email=signupModel.email,
                       )
                user.set_password(signupModel.password)
                user.save()
                setup_user_permissions_and_groups(user)
                user.save()
            except Exception as e:
                form.add_error('__all__', e)
                valid = False
                try:
                    user.delete()
                except:
                    pass
            if valid:
                userProfile = UserProfile(
                    organization=signupModel.organization,
                    zipcode=signupModel.zipcode,
                    user=user
                )
                userProfile.save()
                loginUrl = reverse('admin:login')
                return HttpResponseRedirect(loginUrl)
        return render(request, self.template_name, {'form': form})

def signup(request):
    form = SignupForm()
    data = {
        'form': form,
    }
    return render(template_name='signup.html', context=data, request=request)


def about(request):
    pass


def site_change(request):
    pass