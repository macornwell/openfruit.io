# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('generated_name', models.CharField(null=True, blank=True, max_length=50)),
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
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('continent', models.ForeignKey(to='geography.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='GeoCoordinate',
            fields=[
                ('geocoordinate_id', models.AutoField(serialize=False, primary_key=True)),
                ('lat_integer', openfruit.common.models.IntegerRangeField()),
                ('lat_fractional', models.IntegerField()),
                ('lon_integer', openfruit.common.models.IntegerRangeField()),
                ('lon_fractional', models.IntegerField()),
                ('generated_name', models.CharField(null=True, blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(null=True, blank=True, max_length=30)),
                ('generated_name', models.CharField(null=True, blank=True, max_length=50)),
                ('city', models.ForeignKey(to='geography.City', null=True, blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate', help_text='This is a very specific location.', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('abbreviation', models.CharField(unique=True, max_length=2)),
                ('generated_name', models.CharField(null=True, blank=True, max_length=50)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
            ],
        ),
        migrations.CreateModel(
            name='UserGeographySettings',
            fields=[
                ('user_geography_settings_id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.ForeignKey(to='geography.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('user_location_id', models.AutoField(serialize=False, primary_key=True)),
                ('last_used', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('location', models.ForeignKey(to='geography.Location')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('last_used',),
            },
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('us_zipcode_id', models.AutoField(serialize=False, primary_key=True)),
                ('zipcode', openfruit.common.models.IntegerRangeField(unique=True)),
                ('city', models.ForeignKey(to='geography.City')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
                ('generated_name', models.CharField(null=True, blank=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(to='geography.State', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='zipcode',
            field=models.ForeignKey(to='geography.Zipcode', null=True, blank=True),
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
            name='userlocation',
            unique_together=set([('user', 'location')]),
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
