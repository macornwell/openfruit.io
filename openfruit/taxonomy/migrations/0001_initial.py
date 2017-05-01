# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
import sorl.thumbnail.fields
import openfruit.taxonomy.models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cultivar',
            fields=[
                ('cultivar_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('origin_year', models.IntegerField(null=True, blank=True)),
                ('origin_exact', models.BooleanField(default=True)),
                ('color_dominate_hex', models.CharField(null=True, max_length=6)),
                ('color_secondary_hex', models.CharField(null=True, max_length=6)),
                ('color_tertiary_hex', models.CharField(null=True, max_length=6)),
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, blank=True, upload_to='featured-images')),
                ('chromosome_count', models.IntegerField(null=True, blank=True)),
                ('brief_description', models.CharField(null=True, blank=True, max_length=50)),
                ('history', models.TextField(null=True, blank=True)),
                ('origin_location', models.ForeignKey(to='geography.Location', null=True, blank=True)),
                ('parent_a', models.ForeignKey(related_name='first_children', to='taxonomy.Cultivar', null=True, blank=True)),
                ('parent_b', models.ForeignKey(related_name='second_children', to='taxonomy.Cultivar', null=True, blank=True)),
            ],
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('genus_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(null=True, blank=True, max_length=30)),
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, blank=True, upload_to='featured-images')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='GenusImage',
            fields=[
                ('genus_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='genus-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, blank=True, max_length=300)),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('kingdom_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('featured_image', models.ImageField(null=True, blank=True, upload_to='featured-images')),
            ],
            options={
                'ordering': ('latin_name',),
            },
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('species_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('can_scale_with_pruning', models.BooleanField(default=False)),
                ('years_till_full_size', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('full_size_height', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('full_size_width', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('years_till_first_production', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('years_till_full_production', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, blank=True, upload_to='featured-images')),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
                ('origin', models.ForeignKey(to='geography.Location', null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='SpeciesImage',
            fields=[
                ('species_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='species-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, blank=True, max_length=300)),
                ('species', models.ForeignKey(to='taxonomy.Species')),
            ],
        ),
        migrations.AddField(
            model_name='genus',
            name='kingdom',
            field=models.ForeignKey(to='taxonomy.Kingdom'),
        ),
        migrations.AddField(
            model_name='cultivar',
            name='species',
            field=models.ForeignKey(to='taxonomy.Species'),
        ),
        migrations.AlterUniqueTogether(
            name='species',
            unique_together=set([('genus', 'name')]),
        ),
    ]
