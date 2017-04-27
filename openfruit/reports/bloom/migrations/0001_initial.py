# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BloomReport',
            fields=[
                ('bloom_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('is_profuse', models.BooleanField(default=False)),
                ('was_auto_generated', models.BooleanField(default=False)),
            ],
        ),
    ]
