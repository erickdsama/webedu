import http
import json
from http.cookiejar import logger

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from django.views.generic import RedirectView

from apps.notificaciones.models import Notificacion


class MisNotificacionesListView(LoginRequiredMixin, ListView):
    model = Notificacion
    ordering = ('-pk',)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [{
            'pk': notificacion.pk,
            'fecha': notificacion.fecha.strftime("%d/%m/%Y"),
            'url': notificacion.get_notificacion_url(),
            'visto':notificacion.visto,
            'texto': notificacion.texto,
            'imagen': notificacion.get_image()
        } for notificacion in queryset]
        return JsonResponse(json.dumps(data), status=200, safe=False)

    def get_queryset(self):
        queryset = super(MisNotificacionesListView, self).get_queryset()
        queryset = queryset.filter(usuario=self.request.user)
        return queryset


class NotificacionRedirectView(LoginRequiredMixin, RedirectView):
    notificacion = None

    def get_notificacion(self):
        self.notificacion = get_object_or_404(Notificacion, pk=self.kwargs.get('pk'), usuario=self.request.user)
        return self.notificacion

    def get_redirect_url(self, *args, **kwargs):
        return self.notificacion.url

    def get(self, request, *args, **kwargs):
        notificacion = self.get_notificacion()
        notificacion.visto = True
        notificacion.save()
        return super(NotificacionRedirectView, self).get(request, *args, **kwargs)