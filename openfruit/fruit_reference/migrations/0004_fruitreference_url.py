# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_reference', '0003_fruitreference_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitreference',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]