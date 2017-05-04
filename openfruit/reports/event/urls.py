from django.conf.urls import url
from openfruit.reports.event.views import DistinctEventView

urlpatterns = [
    url('^reports/event/bloom/(?P<id>\d+)?$', DistinctEventView.as_view(event_type='Blooming', url_name='bloom'), name='bloom'),
    url('^reports/event/plant/(?P<id>\d+)?$', DistinctEventView.as_view(event_type='Just Planted', url_name='plant'), name='plant'),
    url('^reports/event/leaf/(?P<id>\d+)?$', DistinctEventView.as_view(event_type='Leafing Out', url_name='leaf'), name='leaf'),
    url('^reports/event/ripe/(?P<id>\d+)?$', DistinctEventView.as_view(event_type='Ripening', url_name='ripe'), name='ripe'),
]
