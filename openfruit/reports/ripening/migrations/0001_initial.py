# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitRipeningReport',
            fields=[
                ('fruit_ripening_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('how_old_is_plant', openfruit.common.models.IntegerRangeField()),
                ('was_auto_generated', models.BooleanField(default=False)),
            ],
        ),
    ]
