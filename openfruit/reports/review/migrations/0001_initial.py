# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitReviewReport',
            fields=[
                ('fruit_review_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('rating', openfruit.common.models.IntegerRangeField()),
                ('text', models.TextField(max_length=1000)),
            ],
        ),
    ]
