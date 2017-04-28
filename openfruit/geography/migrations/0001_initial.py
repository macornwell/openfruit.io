# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('continent_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('continent', models.ForeignKey(to='geography.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='GeoCoordinate',
            fields=[
                ('geocoordinate_id', models.AutoField(primary_key=True, serialize=False)),
                ('lat_integer', openfruit.common.models.IntegerRangeField()),
                ('lat_fractional', models.IntegerField()),
                ('lon_integer', openfruit.common.models.IntegerRangeField()),
                ('lon_fractional', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(null=True, max_length=30, blank=True)),
                ('city', models.ForeignKey(null=True, to='geography.City', blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(null=True, to='geography.GeoCoordinate', blank=True, help_text='This is a very specific location.')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
            ],
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('us_zipcode_id', models.AutoField(primary_key=True, serialize=False)),
                ('zipcode', openfruit.common.models.IntegerRangeField(unique=True)),
                ('city', models.ForeignKey(to='geography.City')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(null=True, to='geography.State', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='zipcode',
            field=models.ForeignKey(null=True, to='geography.Zipcode', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='geocoordinate',
            unique_together=set([('lat_integer', 'lat_fractional', 'lon_integer', 'lon_fractional')]),
        ),
        migrations.AddField(
            model_name='country',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='city',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AlterUniqueTogether(
            name='zipcode',
            unique_together=set([('zipcode', 'geocoordinate')]),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('country', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('country', 'state', 'city', 'zipcode', 'geocoordinate')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('state', 'name')]),
        ),
    ]
