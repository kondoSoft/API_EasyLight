# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_auto_20170718_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipality',
            options={'ordering': ('name_mun',)},
        ),
        migrations.RenameField(
            model_name='municipality',
            old_name='key_state',
            new_name='state',
        ),
    ]
