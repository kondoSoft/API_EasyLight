# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0040_municipality_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
