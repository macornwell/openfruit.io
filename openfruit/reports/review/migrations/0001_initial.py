# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import openfruit.common.models
import openfruit.taxonomy.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geography', '0001_initial'),
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitReviewImage',
            fields=[
                ('fruit_review_image', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='fruit-review-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FruitReviewReport',
            fields=[
                ('fruit_review_report_id', models.AutoField(serialize=False, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('sweet', openfruit.common.models.IntegerRangeField()),
                ('sour', openfruit.common.models.IntegerRangeField()),
                ('bitter', openfruit.common.models.IntegerRangeField(default=1)),
                ('juicy', openfruit.common.models.IntegerRangeField()),
                ('firm', openfruit.common.models.IntegerRangeField()),
                ('was_picked_early', models.BooleanField(default=False)),
                ('rating', openfruit.common.models.IntegerRangeField(null=True, blank=True, help_text='How would you personally rate this fruit?')),
                ('text', models.TextField(null=True, blank=True, help_text='Your opinion about the fruit in your own words.', max_length=1000)),
                ('was_auto_generated', models.BooleanField(default=False)),
                ('cultivar', models.ForeignKey(to='taxonomy.Cultivar', null=True, blank=True)),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
                ('species', models.ForeignKey(to='taxonomy.Species', null=True, blank=True)),
                ('submitted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, openfruit.taxonomy.validators.CultivarSpeciesMixin),
        ),
    ]
