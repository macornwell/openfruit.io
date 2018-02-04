from rest_framework import serializers
from openfruit.taxonomy.models import FruitingPlant, Species, Cultivar


class FruitingPlantSerializer(serializers.ModelSerializer):
    cultivar_name = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    coordinate = serializers.SerializerMethodField()
    details_url = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    def get_cultivar_name(self, obj):
        return str(obj.cultivar)

    def get_species_name(self, obj):
        return str(obj.species)

    def get_coordinate(self, obj):
        return str(obj.geocoordinate)

    def get_details_url(self, obj):
        if obj.cultivar:
            pass
        url = ''

    def get_created_by_name(self, obj):
        return obj.created_by.username

    class Meta:
        model = FruitingPlant
        fields = ('fruiting_plant_id', 'cultivar', 'cultivar_name', 'species', 'species_name', 'date_planted', 'coordinate', 'created_by', 'created_by_name', 'date_died', 'details_url')


class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = ('name', 'latin_name', 'generated_name')


class CultivarSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cultivar
        fields = ('name', 'species', 'generated_name', 'origin_location', 'origin_year', 'uses', 'chromosome_count')
