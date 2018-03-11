from django.conf.urls import url
from openfruit.reports.review import views


urlpatterns = [
    url(r'^api/v1/reports/review/$', views.FruitReviewView.as_view(), name='fruit-review'),
]


