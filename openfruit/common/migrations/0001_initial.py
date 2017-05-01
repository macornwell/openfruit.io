# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('signup_id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=10)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('zipcode', openfruit.common.models.IntegerRangeField(help_text='Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.')),
                ('organization', models.CharField(null=True, blank=True, help_text='If you belong to an organization such as a University, Business or Non-Profit, place it here.', max_length=50)),
                ('request_to_be_a_curator', models.BooleanField(default=False, help_text='If you would like to become a curator.')),
                ('reason_to_be_curator', models.TextField(null=True, blank=True, help_text='A brief explination of why you should be considered for becoming a curator.')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_profile_id', models.AutoField(serialize=False, primary_key=True)),
                ('zipcode', openfruit.common.models.IntegerRangeField(help_text='Your current zipcode will be used as the default location of your records. Use the zipcode where you will be posting from mostly.')),
                ('organization', models.CharField(null=True, blank=True, help_text='If you belong to an organization such as a University, Business or Non-Profit, place it here.', max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
