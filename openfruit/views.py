from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib import messages

from openfruit.dashboard.views import dashboard
from openfruit.reports.event.forms import EventReportForm
from openfruit.taxonomy.models import FruitingPlant
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.geography.services import GEOGRAPHY_DAL


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


def _collect_stats():
    data = {
        'cultivar_count': TAXONOMY_DAL.get_cultivar_count(),
        'location_count': GEOGRAPHY_DAL.get_unique_location_count()
    }
    return data


def home(request):
    if request.user.is_authenticated():
        return dashboard(request)
    data = _collect_stats()
    loginUrl = reverse('admin:login')
    loginNextUrl = escape(request.path)
    data['loginUrl'] = '{0}?next={1}'.format(loginUrl, loginNextUrl)
    return render(template_name='home.html', context=data, request=request)

def about(request):
    return render(template_name='about.html', context={}, request=request)


def site_change(request):
    pass
