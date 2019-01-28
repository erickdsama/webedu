# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 04:48
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25, verbose_name='Nombre(s)')),
                ('apellido_paterno', models.CharField(max_length=25)),
                ('apellido_materno', models.CharField(blank=True, max_length=25, null=True)),
                ('matricula', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'alumno',
                'verbose_name_plural': 'alumnos',
            },
        ),
        migrations.CreateModel(
            name='ContactoEmergencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=55)),
                ('telefono', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{10}', 'Por favor agregué un número telefónico válido')])),
                ('direccion', models.CharField(max_length=140)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contactos_emergencia', to='escuela.Alumno')),
            ],
            options={
                'verbose_name': 'Contacto emergencia',
                'verbose_name_plural': 'Contactos emergencia',
            },
        ),
        migrations.CreateModel(
            name='DiasPracticas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miercoles', 'Miercoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sabado', 'Sabado'), ('Domingo', 'Domingo')], max_length=11)),
                ('hora', models.TimeField()),
            ],
            options={
                'verbose_name': 'Día de práctica',
                'verbose_name_plural': 'Días de práctica',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{10}', 'Por favor agregué un número telefónico válido')])),
                ('activo', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', models.CharField(choices=[('ICSA', 'ICSA'), ('CU', 'CU')], max_length=4)),
                ('nivel', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1)),
                ('grupo', models.CharField(max_length=1)),
                ('horario', models.TextField()),
                ('alumnos', models.ManyToManyField(to='escuela.Alumno')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='escuela.Docente')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='InformacionPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{10}', 'Por favor agregué un número telefónico válido')])),
                ('telefono2', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}', 'Por favor agregué un número telefónico válido')])),
                ('no_servicio_medico', models.CharField(blank=True, max_length=45, null=True)),
                ('tipo_seguro', models.CharField(blank=True, choices=[('Facultativo', 'Facultativo'), ('ICHISAL', 'ICHISAL'), ('IMSS', 'IMSS'), ('ISSSTE', 'ISSSTE'), ('Pensiones', 'Pensiones'), ('Privado', 'Privado')], max_length=11, null=True)),
                ('alumno', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='informacion_personal', to='escuela.Alumno')),
            ],
            options={
                'verbose_name': 'información personal',
                'verbose_name_plural': 'informacion personal',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=85)),
                ('direccion', models.CharField(max_length=140)),
                ('referencia', models.CharField(blank=True, max_length=140, null=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}', 'Por favor agregué un número telefónico válido')])),
                ('contacto_directo', models.CharField(blank=True, max_length=55, null=True)),
                ('contacto_directo_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('responsable_principal', models.CharField(blank=True, max_length=85, null=True)),
                ('nivel', models.CharField(blank=True, max_length=14, null=True)),
                ('subnivel', models.CharField(blank=True, max_length=14, null=True)),
                ('ambito', models.CharField(choices=[('Docencia', 'Docencia'), ('Educación Comunitaria', 'Educación Comunitaria'), ('Educación Especial', 'Educación Especial'), ('Capacitación Industrial y Empresarial', 'Capacitación Industrial y Empresarial'), ('Gestión Educativa', 'Gestión Educativa'), ('Investigación Educativa', 'Investigación Educativa'), ('Gestión Cultural', 'Gestión Cultural')], max_length=45)),
            ],
            options={
                'verbose_name': 'Institucion',
                'verbose_name_plural': 'Instituciones',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.CharField(max_length=4, verbose_name='Año')),
                ('semestre', models.CharField(choices=[('1', '1'), ('2', '2')], max_length=1)),
                ('activo', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Periodo',
                'verbose_name_plural': 'Periodos',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=140)),
                ('modalidad', models.CharField(choices=[('Desarrollo de trayectos profesionales', 'Desarrollo de trayectos profesionales'), ('Emprendimiento', 'Emprendimiento'), ('Estadías Docentes', 'Estadías Docentes'), ('Independiente', 'Independiente'), ('Intervención Educativa', 'Intervención Educativa'), ('Proyecto Independiente', 'Proyecto Independiente')], max_length=37)),
                ('espacio', models.CharField(blank=True, max_length=55, null=True)),
                ('sector', models.CharField(choices=[('Privado', 'Privado'), ('Público', 'Público')], max_length=10)),
                ('tipo', models.CharField(choices=[('Equipo', 'Equipo'), ('Individual', 'Individual'), ('N/A', 'N/A')], max_length=10, verbose_name='Tipo del proyecto')),
                ('beneficiarios', models.CharField(help_text='Categoría', max_length=140)),
                ('beneficiarios_cantidad', models.PositiveIntegerField()),
                ('actividades', models.CharField(blank=True, max_length=255, null=True, verbose_name='Actividades que realiza')),
                ('alumnos', models.ManyToManyField(to='escuela.Alumno')),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyectos', to='escuela.Institucion')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
            },
        ),
        migrations.AddField(
            model_name='grupo',
            name='periodo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='escuela.Periodo'),
        ),
        migrations.AddField(
            model_name='diaspracticas',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dias', to='escuela.Proyecto'),
        ),
    ]