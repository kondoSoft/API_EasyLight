# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 16:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0018_auto_20170725_1647'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='municipality',
            unique_together=set([]),
        ),
    ]
