# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


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
                ('name_denormalized', models.CharField(max_length=50, blank=True)),
                ('latin_name', models.CharField(max_length=50, blank=True)),
                ('chromosome_count', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('brief_description', models.CharField(null=True, max_length=30, blank=True)),
                ('origin_year', models.IntegerField(null=True, blank=True)),
                ('history', models.TextField(null=True, blank=True)),
                ('origin_location', models.ForeignKey(to='geography.Location', null=True, blank=True)),
                ('parent_a', models.ForeignKey(to='taxonomy.Cultivar', related_name='first_children', null=True, blank=True)),
                ('parent_b', models.ForeignKey(to='taxonomy.Cultivar', related_name='second_children', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('genus_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(null=True, max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('kingdom_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('species_id', models.AutoField(serialize=False, primary_key=True)),
                ('latin_name', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
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
