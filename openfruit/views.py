from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib import messages

from openfruit.reports.event.forms import EventReportForm
from openfruit.taxonomy.models import FruitingPlant
from openfruit.taxonomy.services import TAXONOMY_DAL


def testing(request):
    data = {
        'form': EventReportForm(),
    }

    return render(request, 'reports/work/plant.html', data)


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
    if request.user.is_authenticated():
        return dashboard(request)
    data = {}
    loginUrl = reverse('admin:login')
    loginNextUrl = escape(request.path)
    data['loginUrl'] = '{0}?next={1}'.format(loginUrl, loginNextUrl)
    return render(template_name='home.html', context=data, request=request)


def dashboard(request):
    data = {}
    data['users_plants'] = FruitingPlant.objects.get_plants_for_user_that_are_living(request.user)
    data['species_list'] = TAXONOMY_DAL.get_all_species_with_fruiting_plants_of_user(request.user)
    return render(template_name='dashboard.html', context=data, request=request)


def explore_public(request):
    data = {}
    data['public_locations'] = None
    data['species_list'] = TAXONOMY_DAL.get_all_species_with_fruiting_plants()
    return render(template_name='explore.html', context=data, request=request)




def about(request):
    pass


def site_change(request):
    pass