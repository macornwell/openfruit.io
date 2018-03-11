from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, views
from dal import autocomplete
from openfruit.common.services import is_curator
from openfruit.common.serializers import UserSerializer

class EasyRestMixin:
    """
    Provides mixin's for common rest operations.
    """

    def parse_array_query_params(self, request, param):
        """
        Parses the given request's array based query parameters.
        Should be in the format param=[x,y,z] OR param=x
        Regardless, an array is returned.
        :param request:
        :return: An array with the values.
        """
        value = request.query_params.get(param, [])
        if not value:
            return value
        results = []
        if ',' in value:
            results = value.split(',')
        else:
            results.append(value)
        return results


    def query_filter(self, request, queryset, parameter, filter_word=None, default_value=None):
        """
        Conducts a database filter on a given queryset with a given parameter.
        :param request:
        :param queryset:
        :param parameter: Should be a field on a model.
        :param filter_word:
        :param default_value:
        :return:
        """
        value = request.query_params.get(parameter, default_value)
        if value:
            if not filter_word:
                filter_word = parameter
            kwargs = {
                filter_word: value
            }
            queryset = queryset.filter(**kwargs)
        return queryset


class EasyRestDetailAPIView(views.APIView):

    model_type = None
    serializer_type = None

    def get_object(self, pk):
        try:
            return self.model_type.objects.get(pk=pk)
        except self.serializer_type.DoesNotExist:
            raise views.Http404

    def get(self, request, pk, format=None):
        model = self.get_object(pk)
        serializer = self.serializer_type(model, context={'request': request})
        return views.Response(serializer.data)


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



