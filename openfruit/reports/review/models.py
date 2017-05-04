from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField
from openfruit.taxonomy.models import Species, Cultivar
from openfruit.geography.models import Location
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class FruitReviewImage(models.Model):
    fruit_review_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='fruit-review-images')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)


class FruitReviewReport(models.Model, CultivarSpeciesMixin):
    fruit_review_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)
    species = models.ForeignKey(Species, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar, blank=True, null=True)
    sweet = IntegerRangeField(min_value=1, max_value=10)
    sour = IntegerRangeField(min_value=1, max_value=10)
    bitter = IntegerRangeField(min_value=1, max_value=10, default=1)
    juicy = IntegerRangeField(min_value=1, max_value=10)
    firm = IntegerRangeField(min_value=1, max_value=10)
    was_picked_early = models.BooleanField(default=False)
    rating = IntegerRangeField(min_value=1, max_value=5, blank=True, null=True, help_text='How would you personally rate this fruit?')
    text = models.TextField(max_length=1000, blank=True, null=True, help_text='Your opinion about the fruit in your own words.')
    was_auto_generated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.prepare_for_save()
        super(FruitReviewReport, self).save(*args, **kwargs)

    def __str__(self):
        obj = self.cultivar
        if not obj:
            obj = self.species
        return '{0} - {1} rating.'.format(self.datetime, obj.name, self.submitted_by.username, self.rating)


auditlog.register(FruitReviewReport)
auditlog.register(FruitReviewImage)
