from django.shortcuts import render
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.reports.useractivity.services import USER_ACTIVITY_DAL
# Create your views here.


def dashboard(request):
    data = {}
    users_plants = USER_ACTIVITY_DAL.get_all_living_plants_interacted_by(request.user)
    species_with_gmaps_icon = TAXONOMY_DAL.get_species_with_google_maps_images()
    data['users_plants'] = users_plants
    data['species_list'] = set(plant.species for plant in users_plants)
    data['species_to_icon'] = species_with_gmaps_icon
    return render(template_name='dashboard.html', context=data, request=request)
