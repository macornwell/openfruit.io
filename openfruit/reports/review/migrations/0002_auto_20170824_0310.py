# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-24 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0015_auto_20170824_0310'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(old_name='FruitReviewReport', new_name='FruitReview'),
        migrations.RemoveField(
            model_name='fruitreview',
            name='cultivar',
        ),
        migrations.RemoveField(
            model_name='fruitreview',
            name='species',
        ),
        migrations.AddField(
            model_name='fruitreview',
            name='fruiting_plant',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='taxonomy.FruitingPlant'),
            preserve_default=False,
        ),
    ]
