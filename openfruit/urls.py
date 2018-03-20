"""openfruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from openfruit import settings
from openfruit.views import home, about, site_change, testing

router = routers.DefaultRouter()

urlpatterns = [

    url(r'^$', home, name='home'),
    url(r'^about/$', about, name='about'),
    url(r'^terms-of-service/$', TemplateView.as_view(template_name='terms-of-service.html'), name='terms-of-service'),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy-policy.html'), name='privacy-policy'),
    url(r'^request/site-change/$', site_change, name='site_change'),
    url(r'^admin/', include(admin.site.urls), name='admin'),

    # Authorization
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/auth/token/$', obtain_jwt_token),
    url(r'^api/v1/auth/token/verify/$', verify_jwt_token),
    url(r'^api/v1/auth/token/refresh/$', refresh_jwt_token),
    url(r'^api/v1/auth/rest/', include('rest_auth.urls')),
    url(r'^api/v1/auth/allauth/', include('allauth.urls')),
    url(r'^', include('openfruit.ofauth.urls')),

    # Geo
    url(r'^api/v1/', include('django_geo_db.urls')),
    url(r'^api/v1/', include('django_geo_db.autocomplete_urls')),

    url(r'^', include('openfruit.common.urls')),
    url(r'^', include('openfruit.taxonomy.urls')),
    url(r'^', include('openfruit.reports.event.urls')),
    url(r'^', include('openfruit.reports.review.urls')),
    url(r'^', include('openfruit.userdata.urls')),
    url(r'^', include('openfruit.fruit_search.urls')),
    url(r'^', include('openfruit.geography.urls')),
    url(r'^', include('openfruit.fruit_reference.urls')),
    url(r'^', include('openfruit.reports.disease.urls')),
    url(r'^', include('openfruit.fruit_api.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += [url(r'^testing/$', testing, name='testing'),]


