from auditlog.registry import auditlog
from django.db import models
from sorl.thumbnail.fields import ImageField
from colorful.fields import RGBColorField
from openfruit.common.models import IntegerRangeField
from openfruit.geography.models import Location
from openfruit.taxonomy.managers import GenusManager, KingdomManager, SpeciesManager, CultivarManager

PLANT_KINGDOM_NAMES = (
    'Plants', 'Plantae',
)

CHROMOSOME_CHOICES = (
    ('2', 'Diploid x2'),
    ('3', 'Triploid x3'),
    ('4', 'Tetraploid x4'),
    ('5', 'Pentaploid x5'),
    ('6', 'Hexaploid x6'),
    ('8', 'Octoploid x8'),
)

class UrlNameMixin:

    def url_latin_name(self):
        return self.latin_name.replace(' ', '-')

    def url_name(self):
        return self.name.replace(' ', '-')


class Kingdom(models.Model, UrlNameMixin):
    objects = KingdomManager()
    kingdom_id = models.AutoField(primary_key=True)
    latin_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, unique=True)
    featured_image = models.ImageField(upload_to='featured-images', blank=True, null=True)

    def __str__(self):
        return self.latin_name

    class Meta:
        ordering = ('latin_name',)


class Genus(models.Model, UrlNameMixin):
    objects = GenusManager()
    genus_id = models.AutoField(primary_key=True)
    kingdom = models.ForeignKey(Kingdom)
    latin_name = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    featured_image = ImageField(upload_to='featured-images', blank=True, null=True)
    generated_name = models.CharField(max_length=60, unique=True, blank=True, null=True)

    class Meta:
        ordering = ('generated_name',)

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(Genus, self).save(*args, **kwargs)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return '{0} ({1})'.format(self.name, self.latin_name)


class Species(models.Model, UrlNameMixin):
    objects = SpeciesManager()
    species_id = models.AutoField(primary_key=True)
    genus = models.ForeignKey(Genus)
    origin = models.ForeignKey(Location, blank=True, null=True)
    latin_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    can_scale_with_pruning = models.BooleanField(default=False)
    years_till_full_size = IntegerRangeField(min_value=1, max_value=100, blank=True, null=True)
    full_size_height = IntegerRangeField(min_value=1, max_value=500, blank=True, null=True)
    full_size_width = IntegerRangeField(min_value=1, max_value=200, blank=True, null=True)
    years_till_first_production = IntegerRangeField(min_value=1, max_value=30, blank=True, null=True)
    years_till_full_production = IntegerRangeField(min_value=1, max_value=100, blank=True, null=True)
    featured_image = ImageField(upload_to='featured-images', blank=True, null=True)
    generated_name = models.CharField(max_length=60, unique=True, blank=True, null=True)

    class Meta:
        ordering = ('generated_name',)
        unique_together = (('genus', 'name'))

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(Species, self).save(*args, **kwargs)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return '{0} ({1})'.format(self.name, self.latin_name)


class Cultivar(models.Model, UrlNameMixin):
    """
    Metadata information related to a specific clonally propagated piece of fruit.
    This model does NOT contain subjective information or information gathered from in the field.
    """
    objects = CultivarManager()
    cultivar_id = models.AutoField(primary_key=True)
    species = models.ForeignKey(Species)
    name = models.CharField(max_length=40)
    origin_location = models.ForeignKey(Location, blank=True, null=True)
    origin_year = models.IntegerField(blank=True, null=True)
    origin_exact = models.BooleanField(default=True)
    color_dominate_hex = RGBColorField(blank=True, null=True)
    color_secondary_hex = RGBColorField(blank=True, null=True)
    color_tertiary_hex = RGBColorField(blank=True, null=True)
    featured_image = ImageField(upload_to='featured-images', blank=True, null=True)

    # Breeding Information
    chromosome_count = models.CharField(max_length=1, choices=CHROMOSOME_CHOICES, default='2', blank=True, null=True)
    parent_a = models.ForeignKey('Cultivar', blank=True, null=True, related_name='first_children')
    parent_b = models.ForeignKey('Cultivar', blank=True, null=True, related_name='second_children')

    # Descriptive Information
    brief_description = models.CharField(max_length=50, blank=True, null=True)
    history = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.species.name)


class GenusImage(models.Model):
    genus_image_id = models.AutoField(primary_key=True)
    genus = models.ForeignKey(Genus)
    image = ImageField(upload_to='genus-images')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)


class SpeciesImage(models.Model):
    species_image_id = models.AutoField(primary_key=True)
    species = models.ForeignKey(Species)
    image = ImageField(upload_to='species-images')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)




auditlog.register(Kingdom)
auditlog.register(Genus)
auditlog.register(Species)
auditlog.register(Cultivar)
auditlog.register(GenusImage)
auditlog.register(SpeciesImage)
