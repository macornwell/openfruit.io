# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
        ('fruit_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitprofileimage',
            name='cultivar',
            field=models.ForeignKey(to='taxonomy.Cultivar'),
        ),
        migrations.AddField(
            model_name='fruitprofileimage',
            name='species',
            field=models.ForeignKey(to='taxonomy.Species'),
        ),
    ]
