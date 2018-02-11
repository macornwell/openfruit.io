from rest_framework import serializers
from openfruit.taxonomy.models import FruitingPlant, Species, Cultivar, FruitUsageType


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
    species = serializers.SerializerMethodField()
    species_latin = serializers.SerializerMethodField()
    uses = serializers.SerializerMethodField()
    origin_location = serializers.SerializerMethodField()
    ripens_early = serializers.SerializerMethodField()
    ripens_late = serializers.SerializerMethodField()

    def get_species(self, obj):
        return obj.species.name

    def get_species_latin(self, obj):
        return obj.species.latin_name

    def get_ripens_early(self, obj):
        return obj.get_ripens_early_display()

    def get_ripens_late(self, obj):
        return obj.get_ripens_late_display()

    def get_origin_location(self, obj):
        result = {
            'city': None,
            'state': None,
            'country': None,
            'zipcode': None,
            'geocoordinate': None,
        }
        location = obj.origin_location
        if location:
            if location.city:
                result['city'] = location.city.name
            if location.state:
                result['state'] = location.state.abbreviation
            if location.country:
                result['country'] = location.country.abbreviation
            if location.zipcode:
                result['zipcode'] = location.zipcode.zipcode
            if location.geocoordinate:
                result['geocoordinate'] = '{0} {1}'.format(location.geocoordinate.lat, location.geocoordinate.lon)
        return result

    def get_uses(self, obj):
        use_list = []
        if obj.uses:
            for use in obj.uses.all():
                use_list.append(use.type)
        return use_list

    class Meta:
        model = Cultivar
        fields = ('name', 'species', 'species_latin', 'generated_name', 'origin_location',
                  'origin_year', 'uses', 'chromosome_count', 'ripens_early', 'ripens_late')


class FruitUsageTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FruitUsageType
        fields = ('type',)
