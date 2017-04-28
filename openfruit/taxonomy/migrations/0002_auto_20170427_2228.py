# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='species',
            old_name='full_size_in_height',
            new_name='full_size_height',
        ),
        migrations.RenameField(
            model_name='species',
            old_name='full_size_in_width',
            new_name='full_size_width',
        ),
    ]
