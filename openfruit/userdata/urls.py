from django.conf.urls import url
from rest_framework import routers
from openfruit.userdata.views import SignupFormView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^signup/$', SignupFormView.as_view(), name='signup'),
]
