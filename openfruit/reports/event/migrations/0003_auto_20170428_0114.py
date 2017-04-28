# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20170427_2228'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventImage',
        ),
        migrations.AddField(
            model_name='eventreport',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default=1, upload_to='event-images'),
            preserve_default=False,
        ),
    ]
