# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_auto_20170427_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenusImage',
            fields=[
                ('genus_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='genus-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, null=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SpeciesImage',
            fields=[
                ('species_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='species-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, null=True, max_length=300)),
            ],
        ),
        migrations.AlterModelOptions(
            name='genus',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='cultivar',
            name='featured_image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='featured-images'),
        ),
        migrations.AddField(
            model_name='genus',
            name='featured_image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='featured-images'),
        ),
        migrations.AddField(
            model_name='kingdom',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='featured-images'),
        ),
        migrations.AddField(
            model_name='species',
            name='featured_image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='featured-images'),
        ),
        migrations.AddField(
            model_name='speciesimage',
            name='species',
            field=models.ForeignKey(to='taxonomy.Species'),
        ),
        migrations.AddField(
            model_name='genusimage',
            name='genus',
            field=models.ForeignKey(to='taxonomy.Genus'),
        ),
    ]
