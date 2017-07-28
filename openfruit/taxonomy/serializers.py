from rest_framework import serializers
from openfruit.taxonomy.models import FruitingPlant, Species, Cultivar


class FruitingPlantSerializer(serializers.ModelSerializer):
    cultivar_name = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    coordinate = serializers.SerializerMethodField()
    manager_username = serializers.SerializerMethodField()
    details_url = serializers.SerializerMethodField()

    def get_cultivar_name(self, obj):
        return str(obj.cultivar)

    def get_species_name(self, obj):
        return str(obj.species)

    def get_coordinate(self, obj):
        return str(obj.geocoordinate)

    def get_manager_username(self, obj):
        return str(obj.user_manager.username)

    def get_details_url(self, obj):
        if obj.cultivar:
            pass
        url = ''

    class Meta:
        model = FruitingPlant
        fields = ('fruiting_plant_id', 'cultivar', 'cultivar_name', 'species', 'species_name', 'planted', 'coordinate', 'manager_username')





class SpeciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Species
        fields = ('name', 'latin_name', 'generated_name')


class CultivarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cultivar
        fields = ('name', 'species', 'generated_name')
