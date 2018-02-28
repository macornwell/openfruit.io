# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_reference', '0007_auto_20180220_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruitreference',
            name='cultivar_list',
            field=models.ManyToManyField(blank=True, to='taxonomy.Cultivar'),
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='publish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='species_list',
            field=models.ManyToManyField(blank=True, to='taxonomy.Species'),
        ),
    ]