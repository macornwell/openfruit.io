# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-24 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0007_auto_20170824_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='geocoordinate',
            name='lat_neg',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='geocoordinate',
            name='lon_neg',
            field=models.BooleanField(default=False),
        ),
    ]
