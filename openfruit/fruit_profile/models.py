from django.db import models
from openfruit.taxonomy.models import Species, Cultivar


class FruitProfileImage(models.Model):
    fruit_profile_image = models.AutoField(primary_key=True)
    species = models.ForeignKey(Species)
    cultivar = models.ForeignKey(Cultivar)
    image = models.ImageField(upload_to='fruit_profile_images', null=True)

