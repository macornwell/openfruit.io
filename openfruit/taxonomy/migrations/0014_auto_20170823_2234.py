# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-23 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0013_auto_20170823_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fruitingplant',
            old_name='user_manager',
            new_name='user_creator',
        ),
    ]
