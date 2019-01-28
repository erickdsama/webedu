# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-07-19 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0010_auto_20170620_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='escuela.Supervisor'),
        ),
    ]
