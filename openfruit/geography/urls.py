from django.conf.urls import url
from rest_framework import routers
from openfruit.geography import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^location/(?P<id>\d+)?$', views.LocationDetailView.as_view(), name='location-detail'),
]
