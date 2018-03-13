from django.conf.urls import url
from openfruit.fruit_api import views


urlpatterns = [
    url(r'^api/v1/fruits/cultivars/$', views.CultivarQuery.as_view(), name='cultivar-query'),
]


