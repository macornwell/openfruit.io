<<<<<<< HEAD

from rest_framework.generics import ListAPIView

from openfruit.common.views import EasyRestMixin, EasyRestDetailAPIView
from openfruit.fruit_reference.models import FruitReference, FruitReferenceType, Author
from openfruit.fruit_reference.serializers import AuthorSerializer, FruitReferenceSerializer, \
    FruitReferenceTypeSerializer


class FruitReferenceListView(EasyRestMixin, ListAPIView):
    queryset = FruitReference.objects.all()
    serializer_class = FruitReferenceSerializer

    def get_queryset(self):
        queryset = FruitReference.objects.all()
        queryset = self.query_filter(self.request, queryset, 'type', 'type__type')
        queryset = self.query_filter(self.request, queryset, 'author', 'author__name__iexact')
        queryset = self.query_filter(self.request, queryset, 'title')
        return queryset


class FruitReferenceDetailView(EasyRestDetailAPIView):
    model_type = FruitReference
    serializer_type = FruitReferenceSerializer


class FruitReferenceTypeListView(EasyRestMixin, ListAPIView):
    queryset = FruitReferenceType.objects.all()
    serializer_class = FruitReferenceTypeSerializer

    def get_queryset(self):
        queryset = FruitReferenceType.objects.all()
        return queryset


class FruitReferenceTypeDetailView(EasyRestDetailAPIView):
    model_type = FruitReferenceType
    serializer_type = FruitReferenceTypeSerializer


class AuthorListView(EasyRestMixin, ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = Author.objects.all()
        return queryset


class AuthorDetailView(EasyRestDetailAPIView):
    model_type = Author
    serializer_type = AuthorSerializer

=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 89983d2da810c54c65f4fba8252075799ca95cba
