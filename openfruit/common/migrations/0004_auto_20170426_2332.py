# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0003_auto_20170426_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('signup_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(unique=True, max_length=10)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('zipcode', openfruit.common.models.IntegerRangeField(help_text='Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.')),
                ('organization', models.CharField(blank=True, help_text='If you belong to an organization such as a University, Business or Non-Profit, place it here.', max_length=50, null=True)),
                ('request_to_be_a_curator', models.BooleanField(help_text='If you would like to become a curator.', default=False)),
                ('reason_to_be_curator', models.TextField(blank=True, help_text='A brief explination of why you should be considered for becoming a curator.', null=True)),
                ('user', models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='reason_to_be_curator',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='request_to_be_a_curator',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
