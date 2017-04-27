# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import openfruit.taxonomy.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
        ('geography', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventReport',
            fields=[
                ('event_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('was_auto_generated', models.BooleanField(default=False)),
                ('cultivar', models.ForeignKey(null=True, to='taxonomy.Cultivar', blank=True)),
            ],
            bases=(models.Model, openfruit.taxonomy.validators.CultivarSpeciesMixin),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('event_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=15)),
                ('description', models.TextField(null=True, blank=True)),
                ('passed_tense', models.CharField(help_text='The passed tense of the event word. Example: Bloomed', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='eventreport',
            name='event_type',
            field=models.ForeignKey(to='event.EventType'),
        ),
        migrations.AddField(
            model_name='eventreport',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='eventreport',
            name='species',
            field=models.ForeignKey(null=True, to='taxonomy.Species', blank=True),
        ),
        migrations.AddField(
            model_name='eventreport',
            name='submitted_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
