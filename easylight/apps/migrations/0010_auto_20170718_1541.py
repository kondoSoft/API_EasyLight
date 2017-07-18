# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_auto_20170718_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='consumption_name',
            field=models.CharField(choices=[('Consumo Basico', 'Consumo Básico'), ('Consumo Intermedio', 'Consumo Intermedio'), ('Consumo Intermedio Alto', 'Consumo Intermedio Alto'), ('Consumo Excedente', 'Consumo Excedente')], max_length=30),
        ),
        migrations.AlterField(
            model_name='rate',
            name='period_name',
            field=models.CharField(choices=[('Verano', 'Verano'), ('NoVerano', 'Fuera de Verano')], max_length=20),
        ),
    ]
