# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitCharacteristicReport',
            fields=[
                ('fruit_characteristic_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('sweet', openfruit.common.models.IntegerRangeField()),
                ('sour', openfruit.common.models.IntegerRangeField()),
                ('bitter', openfruit.common.models.IntegerRangeField(default=1)),
                ('juicy', openfruit.common.models.IntegerRangeField()),
                ('firm', openfruit.common.models.IntegerRangeField()),
                ('was_picked_early', models.BooleanField(default=False)),
                ('was_auto_generated', models.BooleanField(default=False)),
            ],
        ),
    ]
