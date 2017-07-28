# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-18 17:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0004_auto_20170518_1726'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taxonomy', '0002_auto_20170510_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitingPlant',
            fields=[
                ('fruiting_plant_id', models.AutoField(primary_key=True, serialize=False)),
                ('planted', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='cultivar',
            options={'ordering': ('generated_name',)},
        ),
        migrations.AddField(
            model_name='cultivar',
            name='generated_name',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='fruitingplant',
            name='cultivar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Cultivar'),
        ),
        migrations.AddField(
            model_name='fruitingplant',
            name='geocoordinate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='fruitingplant',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geography.Location'),
        ),
        migrations.AddField(
            model_name='fruitingplant',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taxonomy.Species'),
        ),
        migrations.AddField(
            model_name='fruitingplant',
            name='user_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
