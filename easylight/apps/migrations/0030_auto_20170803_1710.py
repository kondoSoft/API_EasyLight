# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-03 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0029_auto_20170802_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='receipt',
        ),
        migrations.AddField(
            model_name='receipt',
            name='contract',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='apps.Contract'),
            preserve_default=False,
        ),
    ]
