# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-17 16:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_auto_20171012_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 16, 54, 13, 447468, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
