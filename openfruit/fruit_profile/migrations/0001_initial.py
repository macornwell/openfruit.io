# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitProfileImage',
            fields=[
                ('fruit_profile_image', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to='fruit_profile_images')),
            ],
        ),
    ]
