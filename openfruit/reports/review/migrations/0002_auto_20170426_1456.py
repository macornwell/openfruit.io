# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
        ('geography', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitreviewreport',
            name='cultivar',
            field=models.ForeignKey(to='taxonomy.Cultivar', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fruitreviewreport',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='fruitreviewreport',
            name='species',
            field=models.ForeignKey(to='taxonomy.Species', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fruitreviewreport',
            name='submitted_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
