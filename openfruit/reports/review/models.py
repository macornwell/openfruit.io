from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_geo_db.models import Location
from auditlog.registry import auditlog
from openfruit.common.models import IntegerRangeField
from openfruit.taxonomy.models import FruitingPlant, Cultivar
from openfruit.taxonomy.validators import CultivarSpeciesMixin


class FruitReviewImage(models.Model):
    fruit_review_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='fruit-review-images')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class FruitReview(models.Model):
    """
    A review for an individual plant's fruits, OR in an in general cultivar.
    """
    fruit_review_report_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User)
    datetime = models.DateTimeField(default=timezone.now)
    fruiting_plant = models.ForeignKey(FruitingPlant, blank=True, null=True)
    cultivar = models.ForeignKey(Cultivar)
    sweet = IntegerRangeField(min_value=1, max_value=10, default=5)
    sour = IntegerRangeField(min_value=1, max_value=10, default=5)
    bitter = IntegerRangeField(min_value=1, max_value=10, default=1)
    juicy = IntegerRangeField(min_value=1, max_value=10, default=5)
    firm = IntegerRangeField(min_value=1, max_value=10, default=5)
    was_picked_early = models.BooleanField(default=False)
    rating = IntegerRangeField(min_value=1, max_value=5, blank=True, null=True, help_text='How would you personally rate this fruit?')
    text = models.TextField(max_length=1000, blank=True, null=True, help_text='Your opinion about the fruit in your own words.')
    was_auto_generated = models.BooleanField(default=False)

    def __validate(self):
        if not self.cultivar and not self.fruiting_plant:
            raise Exception('Must have a cultivar or a fruiting plant')
        if self.cultivar and self.fruiting_plant:
            if self.fruiting_plant.cultivar is not self.cultivar:
                raise Exception('Must have the same cultivar for the fruiting plant and the cultivar.')

    def __clean_values(self):
        if self.fruiting_plant:
            self.cultivar = self.fruiting_plant.cultivar

    def save(self, *args, **kwargs):
        self.__validate()
        self.__clean_values()
        super(FruitReview, self).save(*args, **kwargs)

    def __str__(self):
        plant = self.fruiting_plant
        if not plant:
            plant = self.cultivar
        return '{0} - {1} review by {2}: {3} {4} {5} {6} {7}'.format(
            self.datetime,
            str(plant),
            self.submitted_by.username,
            self.sweet,
            self.sour,
            self.bitter,
            self.juicy,
            self.firm
        )


auditlog.register(FruitReview)
auditlog.register(FruitReviewImage)
