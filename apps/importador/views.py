from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.conf import settings
from sendfile import sendfile

from apps.importador.procesador import ProcesadorAlumnos, ProcesadorAlumnos2
from .forms import ImportadorForm, ProcesarImportacionForm

from apps.importador.models import Importacion


class ImportarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'importador-form.html'
    model = Importacion
    form_class = ImportadorForm

    def get_success_url(self):
        importacion = Importacion.objects.last()
        return reverse('importador:procesar-importacion', args=[importacion.pk,])

    def form_valid(self, form):
        messages.success(self.request, 'El archivo se subió correctamente')
        importacion = form.save(commit=False)
        importacion.usuario = self.request.user
        importacion.save()
        return super(ImportarCreateView, self).form_valid(form)

class ProcesarImportacionView(LoginRequiredMixin, UpdateView):
    template_name = 'procesar-importacion.html'
    form_class = ProcesarImportacionForm
    model = Importacion
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(ProcesarImportacionView, self).get_context_data(**kwargs)
        procesadorAlumnos = ProcesadorAlumnos2(self.object.archivo.path)
        data.update({'alumnos':procesadorAlumnos.get_alumnos_list()})
        return data

    def form_valid(self, form):
        procesadorAlumnos = ProcesadorAlumnos2(self.object.archivo.path)
        procesadorAlumnos.guardar_alumnos()
        self.object = form.save()
        self.object.importados_num = len(procesadorAlumnos.alumnos)
        self.object.alumnos_creados = procesadorAlumnos.alumnos_creados
        self.object.alumnos_actualizados = procesadorAlumnos.alumnos_actualizados
        self.object.save()
        messages.success(self.request, "Se crearon {} alumnos y se actualizaron {}".format(procesadorAlumnos.alumnos_creados, procesadorAlumnos.alumnos_actualizados))
        return super(ProcesarImportacionView, self).form_valid(form)

class DownloadFormatView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        file_root = settings.MEDIA_ROOT + '/formato-importacion-alumnos.xlsx'
        return sendfile(request, file_root, True)



# IMPORTACION DE INSTITUCIONES

