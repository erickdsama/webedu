# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-28 19:47
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0005_alumno_nivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='matricula',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='contactoemergencia',
            name='telefono',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{7,10}', 'Por favor agregué un número telefónico válido')]),
        ),
        migrations.AlterField(
            model_name='docente',
            name='telefono',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{7,10}', 'Por favor agregué un número telefónico válido')]),
        ),
        migrations.AlterField(
            model_name='informacionpersonal',
            name='telefono',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{7,10}', 'Por favor agregué un número telefónico válido')]),
        ),
        migrations.AlterField(
            model_name='informacionpersonal',
            name='telefono2',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{7,10}', 'Por favor agregué un número telefónico válido')]),
        ),
        migrations.AlterField(
            model_name='institucion',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{7,10}', 'Por favor agregué un número telefónico válido')]),
        ),
    ]