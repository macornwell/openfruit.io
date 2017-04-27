from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from openfruit import settings
from openfruit.views import home, SignupFormView, about, site_change
from openfruit.taxonomy.views import SpeciesFormView, SpeciesListView, CultivarListView, \
    GenusListView, CultivarFormView, GenusFormView, KingdomListView, GenusDetailView


urlpatterns = [
    url(r'^browse/$', KingdomListView.as_view(), name='kingdom-list'),
    url(r'^browse/(?P<kingdom>[a-zA-Z]+)$', GenusListView.as_view(), name='genus-list'),
    url(r'^browse/(?P<kingdom>[a-zA-Z]+)/(?P<genus>[a-zA-Z]+)$', GenusDetailView.as_view(), name='genus-detail'),

    url(r'^species$', SpeciesListView.as_view(), name='species-list'),
    url(r'^species/(?P<species>.+)$', SpeciesFormView.as_view(), name='species-detail'),

    url(r'^cultivars$', CultivarListView.as_view(), name='cultivar-list'),
    url(r'^cultivars/(?P<cultivar>.+)$', CultivarFormView.as_view(), name='cultivar-detail'),
]

