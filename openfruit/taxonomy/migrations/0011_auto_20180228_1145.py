# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-28 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0010_auto_20180219_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='google_maps_image_url',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]