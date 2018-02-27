from rest_framework import serializers
from openfruit.fruit_reference.models import FruitReference, FruitReferenceType, Author


class FruitReferenceSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.type.type


    class Meta:
        model = FruitReference
        fields = ('fruit_reference_id', 'title', 'reference', 'url', 'type', 'author', 'publish_date')


class FruitReferenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FruitReferenceType
        fields = ('type',)


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'website_url')

