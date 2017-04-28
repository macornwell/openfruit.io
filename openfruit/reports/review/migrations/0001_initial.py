# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
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
            name='FruitReviewReport',
            fields=[
                ('fruit_review_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('sweet', openfruit.common.models.IntegerRangeField()),
                ('sour', openfruit.common.models.IntegerRangeField()),
                ('bitter', openfruit.common.models.IntegerRangeField(default=1)),
                ('juicy', openfruit.common.models.IntegerRangeField()),
                ('firm', openfruit.common.models.IntegerRangeField()),
                ('was_picked_early', models.BooleanField(default=False)),
                ('rating', openfruit.common.models.IntegerRangeField(help_text='How would you personally rate this fruit?', null=True, blank=True)),
                ('text', models.TextField(help_text='Your opinion about the fruit in your own words.', null=True, max_length=1000, blank=True)),
                ('was_auto_generated', models.BooleanField(default=False)),
                ('cultivar', models.ForeignKey(null=True, to='taxonomy.Cultivar', blank=True)),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
                ('species', models.ForeignKey(null=True, to='taxonomy.Species', blank=True)),
                ('submitted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, openfruit.taxonomy.validators.CultivarSpeciesMixin),
        ),
    ]
