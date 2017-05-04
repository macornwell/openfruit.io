# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import django.utils.timezone
import openfruit.taxonomy.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0001_initial'),
        ('taxonomy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventReport',
            fields=[
                ('event_report_id', models.AutoField(serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('was_auto_generated', models.BooleanField(default=False)),
                ('affinity', models.IntegerField(choices=[(-1, 'Bad'), (0, 'Neutral'), (1, 'Good')], default=0)),
                ('notes', models.TextField(null=True, blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(null=True, upload_to='event-images', blank=True)),
                ('cultivar', models.ForeignKey(null=True, to='taxonomy.Cultivar', blank=True)),
            ],
            bases=(models.Model, openfruit.taxonomy.validators.CultivarSpeciesMixin),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('event_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=15)),
                ('description', models.TextField(null=True, blank=True)),
                ('passed_tense', models.CharField(max_length=20, help_text='The passed tense of the event word. Example: Bloomed')),
            ],
        ),
        migrations.AddField(
            model_name='eventreport',
            name='event_type',
            field=models.ForeignKey(to='event.EventType'),
        ),
        migrations.AddField(
            model_name='eventreport',
            name='location',
            field=models.ForeignKey(to='geography.Location'),
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
