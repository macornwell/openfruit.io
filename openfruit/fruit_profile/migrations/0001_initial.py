# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitProfileImage',
            fields=[
                ('fruit_profile_image', models.AutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to='fruit_profile_images')),
                ('cultivar', models.ForeignKey(to='taxonomy.Cultivar')),
                ('species', models.ForeignKey(to='taxonomy.Species')),
            ],
        ),
    ]
