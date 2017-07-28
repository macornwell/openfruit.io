from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from dal import autocomplete
from openfruit.common.services import is_curator
from openfruit.common.serializers import UserSerializer


class BaseAutocompleteQuerysetView(autocomplete.Select2QuerySetView):
    model_type = None

    def filter(self, qs):
        """
        This must be implemented
        :param qs:
        :return:
        """
        raise NotImplemented()

    def get_queryset(self):
        qs = self.model_type.objects.all()
        if not self.request.user.is_authenticated():
            return qs
        if self.q:
            qs = self.model_type.objects.all()
            qs = self.filter(qs)
        return qs


class NameAutocomplete(BaseAutocompleteQuerysetView):
    is_contains = False

    def filter(self, qs):
        if self.is_contains:
            qs = qs.filter(name__contains=self.q)
        else:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GeneratedNameAutocomplete(BaseAutocompleteQuerysetView):
    is_contains = False

    def filter(self, qs):
        if self.is_contains:
            qs = qs.filter(generated_name__contains=self.q)
        else:
            qs = qs.filter(generated_name__istartswith=self.q)
        return qs



class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.order_by('username').all()

        if self.q:
            qs = qs.filter(
                Q(username__contains=self.q)
            )
        return qs

class CuratorOnlyUserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.none()
        if is_curator(self.request.user):
            qs = User.objects.order_by('username').all()
        else:
            qs = User.objects.get(user=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(username__contains=self.q)
            )
        return qs


"""
REST Framework Views
"""

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()



