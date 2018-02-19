# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-18 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0007_auto_20180218_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultivar',
            name='ripens_early',
            field=models.IntegerField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'), (-1, 'Unknown')], default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='cultivar',
            name='ripens_late',
            field=models.IntegerField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'), (-1, 'Unknown')], default=-1, null=True),
        ),
    ]