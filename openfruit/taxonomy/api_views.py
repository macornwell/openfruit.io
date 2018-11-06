from rest_framework import generics, status
from rest_framework.views import APIView, Response, Http404

from openfruit.taxonomy.models import Species, Cultivar, Genus, Kingdom, FruitingPlant, \
    FruitUsageType, RIPENING_MONTH_CHOICES, CHROMOSOME_CHOICES
from openfruit.taxonomy.services import TAXONOMY_DAL
from openfruit.taxonomy.serializers import SpeciesSerializer, CultivarSerializer, \
    FruitingPlantSerializer, FruitUsageTypeSerializer, GenusSerializer

################
# Rest Framework
################

class PlantsListView(generics.ListAPIView):
    serializer_class = FruitingPlantSerializer
    pagination_class = None

    def get_queryset(self):
        query_results = TAXONOMY_DAL.query_fruiting_plants(self.request.query_params)
        return query_results


class UsersPlantsListView(generics.ListAPIView):
    serializer_class = FruitingPlantSerializer

    def get_queryset(self):
        species = self.request.query_params.get('species', None)
        return TAXONOMY_DAL.query_users_fruiting_plants(self.request.user, species)


class PublicPlantsView(generics.ListAPIView):
    serializer_class = FruitingPlantSerializer

    def get_queryset(self):
        return TAXONOMY_DAL.public_plants_query(self.request.user, self.request.query_params)


class CultivarDetail(APIView):
    def get_object(self, pk):
        try:
            return Cultivar.objects.get(pk=pk)
        except Cultivar.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CultivarSerializer(snippet, context={'request': request})
        return Response(serializer.data)


class CultivarDetailByName(APIView):
    def get_object(self, name, species):
        try:
            return Cultivar.objects.get(name__iexact=name, species__name__iexact=species)
        except Cultivar.DoesNotExist:
            raise Http404

    def get(self, request, name, species, format=None):
        obj = self.get_object(name, species)
        serializer = CultivarSerializer(obj, context={'request': request})
        return Response(serializer.data)


class SpeciesDetail(APIView):
    def get_object(self, pk):
        try:
            return Species.objects.get(pk=pk)
        except Species.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SpeciesSerializer(snippet)
        return Response(serializer.data)


class GenusDetail(APIView):
    def get_object(self, pk):
        try:
            return Genus.objects.get(pk=pk)
        except Genus.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SpeciesSerializer(snippet)
        return Response(serializer.data)


class FruitUsageTypeDetailView(APIView):
    serializer_class = FruitUsageTypeSerializer


class SpeciesListView(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

    def get_queryset(self):
        cultivars__is_null = self.request.query_params.get('cultivars__is_null', None)
        if cultivars__is_null is not None:
            cultivars__is_null = bool(cultivars__is_null)
            if cultivars__is_null:
                raise Exception('Not implemented')
            else:
                queryset = TAXONOMY_DAL.get_all_species_with_cultivars()
        else:
            queryset = Species.objects.all()

        genus = self.request.query_params.get('genus', None)
        if genus:
            queryset = queryset.filter(genus__latin_name__iexact=genus)
        generated_name = self.request.query_params.get('generated_name', None)
        if generated_name:
            queryset = queryset.filter(generated_name__icontains=generated_name)
        limit = self.request.query_params.get('limit', 10)
        if limit:
            queryset = queryset[:int(limit)]
        return queryset


class GenusListView(generics.ListAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer

    def get_queryset(self):
        queryset = Genus.objects.all()
        return queryset


class CultivarListView(generics.ListAPIView):
    queryset = Cultivar.objects.all()
    serializer_class = CultivarSerializer

    def get_queryset(self):
        queryset = Cultivar.objects.all()
        species = self.request.query_params.get('species', None)
        if species:
            queryset = queryset.filter(species__latin_name__iexact=species)
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__iexact=name)
        name_contains = self.request.query_params.get('name_contains', None)
        if name_contains:
            queryset = queryset.filter(name__icontains=name_contains)
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(origin_location__country__name__icontains=country)
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(origin_location__state__name__iexact=state)
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(origin_location__city__name__iexact=city)
        county = self.request.query_params.get('county', None)
        if county:
            queryset = queryset.filter(origin_location__county__name__iexact=county)
        zipcode = self.request.query_params.get('zipcode', None)
        if zipcode:
            queryset = queryset.filter(origin_location__zipcode=zipcode)
        year_low = self.request.query_params.get('year_low', None)
        if year_low:
            queryset = queryset.filter(origin_year__gte=year_low)
        year_high = self.request.query_params.get('year_high', None)
        if year_high:
            queryset = queryset.filter(origin_year__lte=year_high)
        ripening_low = self.request.query_params.get('ripening_low', None)
        if ripening_low:
            queryset = queryset.filter(ripens_early=ripening_low)
        ripening_high = self.request.query_params.get('ripening_high', None)
        if ripening_high:
            queryset = queryset.filter(ripens_late=ripening_high)
        uses = self.request.query_params.get('uses', None)
        if uses:
            use_list = uses.split(',')
            use_objs = FruitUsageType.objects.filter(type__in__iexact=use_list)
            queryset = queryset.filter(uses__in=use_objs)
        chromosomes = self.request.query_params.get('chromosomes', None)
        if chromosomes:
            queryset = queryset.filter(chromosome_count__iexact=chromosomes)
        queryset = queryset.order_by('name')
        return queryset


class RipeningListView(APIView):

    def get(self, request, *args, **kw):
        response = Response(RIPENING_MONTH_CHOICES, status=status.HTTP_200_OK)
        return response


class ChromosomesListView(APIView):

    def get(self, request, *args, **kw):
        response = Response(CHROMOSOME_CHOICES, status=status.HTTP_200_OK)
        return response
