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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from openfruit import settings
from openfruit.views import home, SignupFormView, about, site_change, testing
from openfruit.taxonomy.urls import urlpatterns as TaxonomyURLs
from openfruit.geography.urls import urlpatterns as GeographyUrls

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^signup/$', SignupFormView.as_view(), name='signup'),
    url(r'^about/$', about, name='about'),
    url(r'^request/site-change/$', site_change, name='site_change'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^testing/$', testing, name='testing'),]

urlpatterns += TaxonomyURLs
urlpatterns += GeographyUrls

