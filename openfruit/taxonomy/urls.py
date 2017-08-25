from django.conf.urls import url
from openfruit.taxonomy import views
from openfruit.taxonomy.views import GenusListView, KingdomListView, \
    GenusDetailView, SpeciesDetailView, CultivarDetailView, SpeciesAutocomplete, \
    CultivarAutocomplete, GenusAutocomplete, GenusFormView, PublicPlantsView, FruitingPlantAutocomplete, \
    move_fruiting_plant, FruitingPlantFormView, Cultivar, SpeciesFormView, cultivar_detail_view_redirect, FruitingPlantDetailsView


urlpatterns = [
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)/(?P<cultivar>.+)$', CultivarDetailView.as_view(), name='cultivar-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)$', SpeciesDetailView.as_view(), name='species-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)$', GenusDetailView.as_view(), name='genus-detail'),
    url(r'^browse/(?P<kingdom>.+)$', GenusListView.as_view(), name='genus-list'),
    url(r'^browse/$', KingdomListView.as_view(), name='browse'),

    url(r'^genus/(?P<id>\d+)?$', GenusFormView.as_view(), name='genus'),
    url(r'^genus/(?P<genusID>\d+)/species/(?P<id>\d+)?$', SpeciesFormView.as_view(), name='species'),
    url(r'^cultivar/(?P<cultivar_id>\d+)', cultivar_detail_view_redirect, name='cultivar-detail-redirect'),
    url(r'^fruiting-plant/(?P<id>\d+)?$', FruitingPlantFormView.as_view(), name='fruiting-plant'),
    url(r'^fruiting-plant/details/(?P<id>\d+)?$', FruitingPlantDetailsView.as_view(), name='fruiting-plant-details'),

    url('^autocomplete/genus/$', GenusAutocomplete.as_view(), name='genus-autocomplete'),
    url('^autocomplete/species/$', SpeciesAutocomplete.as_view(), name='species-autocomplete'),
    url('^autocomplete/cultivar/$', CultivarAutocomplete.as_view(model=Cultivar,
            create_field='name',), name='cultivar-autocomplete'),
    url('^autocomplete/fruiting-plant/$', FruitingPlantAutocomplete.as_view(), name='fruiting-plant-autocomplete'),

    url('^api/v1/plants/move$', move_fruiting_plant, name='move_fruiting_plant'),
    url('^api/v1/plants/public/$', PublicPlantsView.as_view(), name='public_plants_without_user'),
    url(r'^api/v1/species/(?P<pk>[0-9]+)/$', views.SpeciesDetail.as_view(), name='species-detail'),
    url(r'^api/v1/cultivar/(?P<pk>[0-9]+)/$', views.CultivarDetail.as_view(), name='cultivar-detail'),
    url(r'^api/v1/fruiting-plants/(?P<query>.+)?$', views.PlantsListView.as_view(), name='users-fruiting-plants'),
]


