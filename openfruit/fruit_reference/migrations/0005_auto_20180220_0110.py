# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_reference', '0004_fruitreference_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruitreference',
            name='reference',
            field=models.TextField(blank=True, null=True),
        ),
    ]