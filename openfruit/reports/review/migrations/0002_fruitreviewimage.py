# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitReviewImage',
            fields=[
                ('fruit_review_image', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='fruit-review-images')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
    ]
