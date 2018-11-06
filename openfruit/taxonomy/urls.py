from django.conf.urls import url
from openfruit.taxonomy import views
from openfruit.taxonomy.views import GenusListView, KingdomListView, \
    GenusDetailView, SpeciesDetailView, CultivarDetailView, SpeciesAutocomplete, \
    CultivarAutocomplete, GenusAutocomplete, GenusFormView, FruitingPlantAutocomplete, \
    move_fruiting_plant, FruitingPlantFormView, Cultivar, SpeciesFormView, cultivar_detail_view_redirect, \
    FruitingPlantDetailsView, search, species_detail_view_redirect

from openfruit.taxonomy import api_views


urlpatterns = [
    url(r'^search/$', search, name='search'),

    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)/(?P<cultivar>.+)$', CultivarDetailView.as_view(), name='browse-cultivar-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)$', SpeciesDetailView.as_view(), name='browse-species-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)$', GenusDetailView.as_view(), name='browse-genus-detail'),
    url(r'^browse/(?P<kingdom>.+)$', GenusListView.as_view(), name='browse-genus-list'),
    url(r'^browse/$', KingdomListView.as_view(), name='browse'),

    url(r'^genus/(?P<id>\d+)?$', GenusFormView.as_view(), name='genus'),
    url(r'^genus/(?P<genusID>\d+)/species/(?P<id>\d+)?$', SpeciesFormView.as_view(), name='species'),
    url(r'^cultivar/(?P<cultivar_id>\d+)', cultivar_detail_view_redirect, name='cultivar-detail-redirect'),
    url(r'^species/(?P<species_id>\d+)', species_detail_view_redirect, name='species-detail-redirect'),

    url(r'^fruiting-plant/(?P<id>\d+)?$', FruitingPlantFormView.as_view(), name='fruiting-plant'),
    url(r'^fruiting-plant/details/(?P<id>\d+)?$', FruitingPlantDetailsView.as_view(), name='fruiting-plant-details'),

    url('^autocomplete/genus/$', GenusAutocomplete.as_view(), name='genus-autocomplete'),
    url('^autocomplete/species/$', SpeciesAutocomplete.as_view(), name='species-autocomplete'),
    url('^autocomplete/cultivar/$', CultivarAutocomplete.as_view(model=Cultivar,
            create_field='name',), name='cultivar-autocomplete'),
    url('^autocomplete/fruiting-plant/$', FruitingPlantAutocomplete.as_view(), name='fruiting-plant-autocomplete'),

    url('^api/v1/plants/move$', move_fruiting_plant, name='move_fruiting_plant'),
    url('^api/v1/plants/public/$', api_views.PublicPlantsView.as_view(), name='public_plants_without_user'),
    url(r'^api/v1/genus/(?P<pk>[0-9]+)/$', api_views.GenusDetail.as_view(), name='genus-detail'),
    url(r'^api/v1/genus_list/$', api_views.GenusListView.as_view(), name='genus-list'),
    url(r'^api/v1/species/(?P<pk>[0-9]+)/$', api_views.SpeciesDetail.as_view(), name='species-detail'),
    url(r'^api/v1/species_list/$', api_views.SpeciesListView.as_view(), name='species-list'),
    url(r'^api/v1/fruit-usage-type/$', api_views.FruitUsageTypeDetailView.as_view(), name='fruitusagetype-detail'),
    url(r'^api/v1/cultivars/$', api_views.CultivarListView.as_view(), name='cultivar-list'),
    url(r'^api/v1/cultivar_list/$', api_views.CultivarListView.as_view(), name='cultivar-list'),
    url(r'^api/v1/cultivars/(?P<pk>[0-9]+)/$', api_views.CultivarDetail.as_view(), name='cultivar-detail'),
    url(r'^api/v1/fruiting-plants/(?P<query>.+)?$', api_views.PlantsListView.as_view(), name='users-fruiting-plants'),
    url(r'^api/v1/ripenings/$', api_views.RipeningListView.as_view(), name='ripenings-list'),
    url(r'^api/v1/chromosomes/$', api_views.ChromosomesListView.as_view(), name='chromosomes-list'),
]


