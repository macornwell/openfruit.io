from django.conf.urls import url
from openfruit.taxonomy.views import GenusListView, KingdomListView, GenusDetailView, SpeciesDetailView, CultivarDetailView


urlpatterns = [
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)/(?P<cultivar>.+)$', CultivarDetailView.as_view(), name='cultivar-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)/(?P<species>.+)$', SpeciesDetailView.as_view(), name='species-detail'),
    url(r'^browse/(?P<kingdom>.+)/(?P<genus>.+)$', GenusDetailView.as_view(), name='genus-detail'),
    url(r'^browse/(?P<kingdom>.+)$', GenusListView.as_view(), name='genus-list'),
    url(r'^browse/$', KingdomListView.as_view(), name='browse'),
]

