# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genus',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
