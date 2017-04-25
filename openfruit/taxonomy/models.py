from auditlog.registry import auditlog
from django.db import models
#from openfruit.common.models import models.Model
from openfruit.geography.models import Location


class Kingdom(models.Model):
    kingdom_id = models.AutoField(primary_key=True)
    latin_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.latin_name


class Genus(models.Model):
    genus_id = models.AutoField(primary_key=True)
    kingdom = models.ForeignKey(Kingdom)
    latin_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name or self.latin_name


class Species(models.Model):
    species_id = models.AutoField(primary_key=True)
    genus = models.ForeignKey(Genus)
    latin_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name or self.latin_name

    class Meta:
        unique_together = (("genus", "name"),)


class Cultivar(models.Model):
    cultivar_id = models.AutoField(primary_key=True)
    species = models.ForeignKey(Species)
    name = models.CharField(max_length=40)
    name_denormalized = models.CharField(max_length=50, blank=True)
    latin_name = models.CharField(max_length=50, blank=True)
    chromosome_count = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brief_description = models.CharField(max_length=30, blank=True, null=True)
    origin_location = models.ForeignKey(Location, blank=True, null=True)
    origin_year = models.IntegerField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)

    #ripening = models.ForeignKey(RipeningDate, default=get_default_ripening_date)

    parent_a = models.ForeignKey('Cultivar', blank=True, null=True, related_name='first_children')
    parent_b = models.ForeignKey('Cultivar', blank=True, null=True, related_name='second_children')


auditlog.register(Kingdom)
auditlog.register(Genus)
auditlog.register(Species)
auditlog.register(Cultivar)
