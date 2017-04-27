# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cultivar',
            fields=[
                ('cultivar_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('origin_year', models.IntegerField(null=True, blank=True)),
                ('origin_exact', models.BooleanField(default=True)),
                ('color_dominate_hex', models.CharField(max_length=6)),
                ('color_secondary_hex', models.CharField(max_length=6)),
                ('color_tertiary_hex', models.CharField(max_length=6)),
                ('chromosome_count', models.IntegerField(null=True, blank=True)),
                ('brief_description', models.CharField(null=True, max_length=50, blank=True)),
                ('history', models.TextField(null=True, blank=True)),
                ('origin_location', models.ForeignKey(null=True, to='geography.Location', blank=True)),
                ('parent_a', models.ForeignKey(null=True, related_name='first_children', to='taxonomy.Cultivar', blank=True)),
                ('parent_b', models.ForeignKey(null=True, related_name='second_children', to='taxonomy.Cultivar', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('genus_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(null=True, max_length=30, blank=True)),
            ],
            options={
                'ordering': ('latin_name',),
            },
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('kingdom_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
            options={
                'ordering': ('latin_name',),
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('species_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('can_scale_with_pruning', models.BooleanField(default=False)),
                ('years_till_full_size', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('full_size_in_height', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('full_size_in_width', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('years_till_first_production', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('years_till_full_production', openfruit.common.models.IntegerRangeField(null=True, blank=True)),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
                ('origin', models.ForeignKey(null=True, to='geography.Location', blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
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
