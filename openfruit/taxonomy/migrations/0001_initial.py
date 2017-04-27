# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cultivar',
            fields=[
                ('cultivar_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('origin_year', models.IntegerField(blank=True, null=True)),
                ('origin_exact', models.BooleanField(default=True)),
                ('color_dominate_hex', models.CharField(max_length=6)),
                ('color_secondary_hex', models.CharField(max_length=6)),
                ('color_tertiary_hex', models.CharField(max_length=6)),
                ('chromosome_count', models.IntegerField(blank=True, null=True)),
                ('brief_description', models.CharField(max_length=50, blank=True, null=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('origin_location', models.ForeignKey(to='geography.Location', null=True, blank=True)),
                ('parent_a', models.ForeignKey(to='taxonomy.Cultivar', null=True, blank=True, related_name='first_children')),
                ('parent_b', models.ForeignKey(to='taxonomy.Cultivar', null=True, blank=True, related_name='second_children')),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('genus_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('kingdom_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('species_id', models.AutoField(primary_key=True, serialize=False)),
                ('latin_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('can_scale_with_pruning', models.BooleanField(default=False)),
                ('years_till_full_size', openfruit.common.models.IntegerRangeField()),
                ('full_size_in_height', openfruit.common.models.IntegerRangeField()),
                ('full_size_in_width', openfruit.common.models.IntegerRangeField()),
                ('years_till_first_production', openfruit.common.models.IntegerRangeField()),
                ('years_till_full_production', openfruit.common.models.IntegerRangeField()),
                ('genus', models.ForeignKey(to='taxonomy.Genus')),
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
