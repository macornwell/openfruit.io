# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-11 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('fruit_reference', '0001_initial'), ('fruit_reference', '0002_auto_20180218_2200'), ('fruit_reference', '0003_fruitreference_title'), ('fruit_reference', '0004_fruitreference_url'), ('fruit_reference', '0005_auto_20180220_0110'), ('fruit_reference', '0006_auto_20180220_0118'), ('fruit_reference', '0007_auto_20180220_0120'), ('fruit_reference', '0008_auto_20180220_0138'), ('fruit_reference', '0009_auto_20180220_0232'), ('fruit_reference', '0010_auto_20180220_2034')]

    dependencies = [
        ('taxonomy', '0007_auto_20180218_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitReference',
            fields=[
                ('fruit_reference_id', models.AutoField(primary_key=True, serialize=False)),
                ('reference', models.TextField()),
                ('author', models.CharField(blank=True, max_length=50, null=True)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FruitReferenceType',
            fields=[
                ('fruit_reference_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='fruitreference',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruit_reference.FruitReferenceType'),
        ),
        migrations.AddField(
            model_name='fruitreference',
            name='cultivar_list',
            field=models.ManyToManyField(blank=True, to='taxonomy.Cultivar'),
        ),
        migrations.AddField(
            model_name='fruitreference',
            name='species_list',
            field=models.ManyToManyField(blank=True, to='taxonomy.Species'),
        ),
        migrations.AddField(
            model_name='fruitreference',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fruitreference',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='reference',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fruit_reference.Author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='publish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='fruitreference',
            unique_together=set([('title', 'type', 'author')]),
        ),
    ]
