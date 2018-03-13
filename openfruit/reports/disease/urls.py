from django.conf.urls import url
from openfruit.reports.disease import views


urlpatterns = [
    url(r'^api/v1/reports/disease-types/$', views.DiseaseTypeListView.as_view(), name='disease-types'),
    url(r'^api/v1/reports/disease-resistances/$', views.DiseaseResistancesView.as_view(), name='disease-resistances'),
]


