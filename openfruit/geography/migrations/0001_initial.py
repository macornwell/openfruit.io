# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('continent_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('continent', models.ForeignKey(to='geography.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location', models.AutoField(serialize=False, primary_key=True)),
                ('latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('city', models.ForeignKey(to='geography.City', null=True, blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(to='geography.Country')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('country', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('state', 'name')]),
        ),
    ]
