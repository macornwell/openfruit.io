from django.contrib import admin
from openfruit.fruit_reference.models import FruitReference, FruitReferenceType, Author

admin.site.register(FruitReference)
admin.site.register(FruitReferenceType)
admin.site.register(Author)
