# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pacientes', '0003_auto_20161124_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento_apoyo',
            name='Donacion_especie',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
