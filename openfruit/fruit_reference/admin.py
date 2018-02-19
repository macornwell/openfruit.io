from django.contrib import admin
from openfruit.fruit_reference.models import FruitReference, FruitReferenceType

admin.site.register(FruitReference)
admin.site.register(FruitReferenceType)
