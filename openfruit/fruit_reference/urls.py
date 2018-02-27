from django.conf.urls import url
from openfruit.fruit_reference import views


urlpatterns = [
    url(r'^api/v1/fruit-references/$', views.FruitReferenceListView.as_view(), name='fruit-references'),
    url(r'^api/v1/fruit-references/(?P<pk>[0-9]+)/$', views.FruitReferenceDetailView.as_view(), name='fruitreference-detail'),
    url(r'^api/v1/fruit-reference-types/$', views.FruitReferenceTypeListView.as_view(), name='fruit-reference-type'),
    url(r'^api/v1/fruit-reference-types/(?P<pk>[0-9]+)/$', views.FruitReferenceTypeDetailView.as_view(), name='fruitreferencetype-detail'),
    url(r'^api/v1/authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^api/v1/authors/(?P<pk>[0-9]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
]


