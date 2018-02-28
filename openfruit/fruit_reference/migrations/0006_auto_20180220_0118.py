# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-20 01:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_reference', '0005_auto_20180220_0110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('website_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='fruitreference',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fruit_reference.Author'),
            preserve_default=False,
        ),
    ]