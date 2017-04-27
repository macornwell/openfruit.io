# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20170426_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='organization',
            field=models.CharField(null=True, max_length=50, help_text='If you belong to an organization such as a University, Business or Non-Profit, place it here.', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reason_to_be_curator',
            field=models.TextField(null=True, help_text='A brief explination of why you should be considered for becoming a curator.', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='request_to_be_a_curator',
            field=models.BooleanField(default=False, help_text='If you would like to become a curator.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zipcode',
            field=openfruit.common.models.IntegerRangeField(help_text='Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.'),
        ),
    ]
