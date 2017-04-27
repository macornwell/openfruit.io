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
                ('fruit_profile_image', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='fruit_profile_images', null=True)),
                ('cultivar', models.ForeignKey(to='taxonomy.Cultivar')),
                ('species', models.ForeignKey(to='taxonomy.Species')),
            ],
        ),
    ]
