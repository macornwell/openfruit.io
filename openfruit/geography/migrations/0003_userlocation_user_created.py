# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0002_location_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlocation',
            name='user_created',
            field=models.BooleanField(default=True),
        ),
    ]
