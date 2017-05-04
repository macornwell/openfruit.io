# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
import sorl.thumbnail.fields
import colorful.fields
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
                ('color_dominate_hex', colorful.fields.RGBColorField(null=True, blank=True)),
                ('color_secondary_hex', colorful.fields.RGBColorField(null=True, blank=True)),
                ('color_tertiary_hex', colorful.fields.RGBColorField(null=True, blank=True)),
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, upload_to='featured-images', blank=True)),
                ('chromosome_count', models.CharField(null=True, choices=[('2', 'Diploid x2'), ('3', 'Triploid x3'), ('4', 'Tetraploid x4'), ('5', 'Pentaploid x5'), ('6', 'Hexaploid x6'), ('8', 'Octoploid x8')], default='2', max_length=1, blank=True)),
                ('brief_description', models.CharField(null=True, max_length=50, blank=True)),
                ('history', models.TextField(null=True, blank=True)),
                ('origin_location', models.ForeignKey(null=True, to='geography.Location', blank=True)),
                ('parent_a', models.ForeignKey(null=True, related_name='first_children', to='taxonomy.Cultivar', blank=True)),
                ('parent_b', models.ForeignKey(null=True, related_name='second_children', to='taxonomy.Cultivar', blank=True)),
            ],
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('genus_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(null=True, max_length=30, blank=True)),
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, upload_to='featured-images', blank=True)),
                ('generated_name', models.CharField(null=True, max_length=60, unique=True, blank=True)),
            ],
            options={
                'ordering': ('generated_name',),
            },
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='GenusImage',
            fields=[
                ('genus_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='genus-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('kingdom_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('featured_image', models.ImageField(null=True, upload_to='featured-images', blank=True)),
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
                ('featured_image', sorl.thumbnail.fields.ImageField(null=True, upload_to='featured-images', blank=True)),
                ('generated_name', models.CharField(null=True, max_length=60, unique=True, blank=True)),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
                ('origin', models.ForeignKey(null=True, to='geography.Location', blank=True)),
            ],
            options={
                'ordering': ('generated_name',),
            },
            bases=(models.Model, openfruit.taxonomy.models.UrlNameMixin),
        ),
        migrations.CreateModel(
            name='SpeciesImage',
            fields=[
                ('species_image_id', models.AutoField(serialize=False, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='species-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
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
