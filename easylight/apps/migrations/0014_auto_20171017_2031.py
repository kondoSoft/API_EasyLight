# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-17 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0013_auto_20171017_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='contracts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.Contract'),
        ),
    ]
