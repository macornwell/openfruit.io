from django.conf.urls import url
from openfruit.fruit_search import views


urlpatterns = [
    url(r'^fruit-search/$', views.fruit_search, name='fruit-search'),
    url(r'^api/v1/fruit-search/(?P<query>.+)?$', views.FruitSearchListView.as_view(), name='fruit-search-api'),
]


