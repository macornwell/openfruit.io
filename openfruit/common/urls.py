from django.conf.urls.static import static
from django.conf.urls import url
from openfruit.common import views

urlpatterns = [
     url('^autocomplete/user/$', views.UserAutocomplete.as_view(),
         name='user-autocomplete'),
     url('^autocomplete/user2/$', views.CuratorOnlyUserAutocomplete.as_view(),
         name='curator-only-user-autocomplete'),

      url(r'^api/v1/users/$',
          views.UserListView.as_view(), name='user-list'),

]