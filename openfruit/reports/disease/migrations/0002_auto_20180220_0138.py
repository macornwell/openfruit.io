# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_reference', '0008_auto_20180220_0138'),
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseResistanceReport',
            fields=[
                ('disease_resistance_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('resistance_level', models.CharField(choices=[('p', 'Poor'), ('f', 'Fair'), ('e', 'Excellent')], max_length=1)),
                ('disease_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disease.DiseaseType')),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruit_reference.FruitReference')),
            ],
        ),
        migrations.RemoveField(
            model_name='diseasereport',
            name='disease_type',
        ),
        migrations.RemoveField(
            model_name='diseasereport',
            name='reference',
        ),
        migrations.DeleteModel(
            name='DiseaseReport',
        ),
    ]