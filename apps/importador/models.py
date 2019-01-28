from django.db import models

from apps.usuarios.models import User


class Importacion(models.Model):
    class Meta:
        verbose_name = 'Importación'
        verbose_name_plural = 'Importaciones'

    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    archivo = models.FileField(upload_to='importaciones')
    procesado = models.BooleanField(default=False)
    importados_num = models.PositiveIntegerField(default=0)
    alumnos_creados = models.PositiveIntegerField(default=0)
    alumnos_actualizados = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.archivo.name


class ImportacionInstituciones(models.Model):
    class Meta:
        verbose_name = 'Importacion de instituciones'
        verbose_name_plural = 'Importaciones de instiruciones'

    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    archivo = models.FileField(upload_to='importaciones')
    procesado = models.BooleanField(default=False)
    importados_num = models.PositiveIntegerField(default=0)
    instituciones_creadas = models.PositiveIntegerField(default=0)
    instituciones_actualizadas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.archivo.name

    def procesarArchivo(self):
        pass