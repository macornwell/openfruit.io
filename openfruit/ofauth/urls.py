from django.conf.urls import url
from django.views.generic import TemplateView
from openfruit.ofauth.social import FacebookLogin


urlpatterns = [

    url(r'^social/login$', TemplateView.as_view(template_name='ofauth/social.html')),

    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
]
