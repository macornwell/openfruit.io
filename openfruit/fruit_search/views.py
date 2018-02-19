from django.shortcuts import render
from openfruit.taxonomy.serializers import CultivarSerializer

from rest_framework.generics import ListAPIView

class PlantsListView(ListAPIView):
    serializer_class = CultivarSerializer

    def get_queryset(self):
        return TAXONOMY_DAL.query_fruiting_plants(self.request.query_params)

