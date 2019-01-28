from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.urls import reverse

from apps.emails.emails import Email
from apps.usuarios.models import User


class Notificacion(models.Model):
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, related_name='notificaciones')
    url = models.URLField()
    texto = models.CharField(max_length=255)
    visto = models.BooleanField(default=False)
    usuario_creo = models.ForeignKey(User, related_name='notificaciones_creadas', blank=True, null=True)

    def __str__(self):
        return self.texto

    def get_image(self):
        if self.usuario_creo:
            return self.usuario_creo.get_image()
        else:
            return False

    def get_notificacion_url(self):
        return reverse('notificaciones:ver-notificacion', args=[self.pk])

    def send_email(self, request=False):
        site = get_current_site(request)
        email = Email('Nueva notificación', {'user':self.usuario, 'notificacion':self, 'site':site},self.usuario.email, 'notificacion.html')
        email.send()