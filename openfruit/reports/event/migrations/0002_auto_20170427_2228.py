# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('event_image', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='event-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='eventreport',
            name='affinity',
            field=models.IntegerField(choices=[(-1, 'Bad'), (0, 'Neutral'), (1, 'Good')], default=0),
        ),
        migrations.AddField(
            model_name='eventreport',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
