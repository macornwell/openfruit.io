# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genus',
            options={'ordering': ('latin_name',)},
        ),
        migrations.AlterModelOptions(
            name='kingdom',
            options={'ordering': ('latin_name',)},
        ),
        migrations.AlterModelOptions(
            name='species',
            options={'ordering': ('name',)},
        ),
    ]
