from django.conf.urls import url
from openfruit.reports.disease import views


urlpatterns = [
    url(r'^api/v1/disease-types/$', views.DiseaseTypeListView.as_view(), name='disease-types'),
]


