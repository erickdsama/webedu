# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importador', '0002_auto_20170131_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='importacion',
            name='alumnos_actualizados',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='importacion',
            name='alumnos_creados',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
