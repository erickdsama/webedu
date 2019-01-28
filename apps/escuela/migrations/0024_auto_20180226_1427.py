# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-26 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0023_institucion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='archivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='institucion',
            name='archivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='archivo',
            field=models.BooleanField(default=False),
        ),
    ]
