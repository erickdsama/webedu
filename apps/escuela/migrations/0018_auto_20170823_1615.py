# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-23 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0017_auto_20170816_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactoemergencia',
            name='direccion',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]
