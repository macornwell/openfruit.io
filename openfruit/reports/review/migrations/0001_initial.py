# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
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
            name='FruitReviewImage',
            fields=[
                ('fruit_review_image', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='fruit-review-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
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
                ('rating', openfruit.common.models.IntegerRangeField(null=True, help_text='How would you personally rate this fruit?', blank=True)),
                ('text', models.TextField(null=True, max_length=1000, help_text='Your opinion about the fruit in your own words.', blank=True)),
                ('was_auto_generated', models.BooleanField(default=False)),
                ('cultivar', models.ForeignKey(null=True, to='taxonomy.Cultivar', blank=True)),
                ('location', models.ForeignKey(to='geography.Location')),
                ('species', models.ForeignKey(null=True, to='taxonomy.Species', blank=True)),
                ('submitted_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, openfruit.taxonomy.validators.CultivarSpeciesMixin),
        ),
    ]
