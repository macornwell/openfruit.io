# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-11 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0003_auto_20180204_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='cultivar',
            name='ripens_early',
            field=models.CharField(blank=True, choices=[('ej', 'Early January'), ('mj', 'January'), ('lj', 'Late January'), ('efe', 'Early February'), ('mfe', 'February'), ('lfe', 'Late February'), ('ema', 'Early March'), ('mma', 'March'), ('lma', 'Late March'), ('eap', 'Early April'), ('map', 'April'), ('lap', 'Late April'), ('emy', 'Early May'), ('mmy', 'May'), ('lmy', 'Late May'), ('eju', 'Early June'), ('mju', 'June'), ('lju', 'Late June'), ('ejy', 'Early July'), ('mjy', 'July'), ('ljy', 'Late July'), ('eau', 'Early August'), ('mau', 'August'), ('lau', 'Late August'), ('ese', 'Early September'), ('mse', 'September'), ('lse', 'Late September'), ('eoc', 'Early October'), ('moc', 'October'), ('loc', 'Late October'), ('eno', 'Early November'), ('mno', 'November'), ('lno', 'Late November'), ('ede', 'Early December'), ('mde', 'December'), ('lde', 'Late December')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='cultivar',
            name='ripens_late',
            field=models.CharField(blank=True, choices=[('ej', 'Early January'), ('mj', 'January'), ('lj', 'Late January'), ('efe', 'Early February'), ('mfe', 'February'), ('lfe', 'Late February'), ('ema', 'Early March'), ('mma', 'March'), ('lma', 'Late March'), ('eap', 'Early April'), ('map', 'April'), ('lap', 'Late April'), ('emy', 'Early May'), ('mmy', 'May'), ('lmy', 'Late May'), ('eju', 'Early June'), ('mju', 'June'), ('lju', 'Late June'), ('ejy', 'Early July'), ('mjy', 'July'), ('ljy', 'Late July'), ('eau', 'Early August'), ('mau', 'August'), ('lau', 'Late August'), ('ese', 'Early September'), ('mse', 'September'), ('lse', 'Late September'), ('eoc', 'Early October'), ('moc', 'October'), ('loc', 'Late October'), ('eno', 'Early November'), ('mno', 'November'), ('lno', 'Late November'), ('ede', 'Early December'), ('mde', 'December'), ('lde', 'Late December')], max_length=3, null=True),
        ),
    ]