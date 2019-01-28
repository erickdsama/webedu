from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView

from apps.escuela.models import Alumno, Proyecto, Institucion


class AlumnoArchivoListView(ListView):
    model = Alumno
    queryset = Alumno.objects.filter(archivo=True)
    template_name = 'alumno-list.html'
    paginate_by = 50
    page_kwarg = 'pagina'


    def get_context_data(self, **kwargs):
        data =  super(AlumnoArchivoListView, self).get_context_data(**kwargs)
        data.update({
            'title_page': 'Alumnos archivados'
        })
        return data


class AlumnoArchivoView(UserPassesTestMixin, DeleteView):
    model = Alumno
    template_name = 'archivar.html'
    success_url = reverse_lazy('escuela:alumnos-list')

    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin() or self.request.user.is_supervisor() or self.request.user.is_capturista():
                return True
        return False

    def get_cancel_url(self):
        return reverse('escuela:alumno-detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'object_type': 'alumno',
            'cancel': self.get_cancel_url()
        })
        obj = self.get_object()
        if obj.archivo:
            kwargs.update({
                'title_page': 'Desarchivar alumno {}'.format(self.get_object().__str__()),
                'action': 'desarchivar'
            })
        else:
            kwargs.update({
                'title_page': 'Archivar alumno {}'.format(self.get_object().__str__()),
                'action': 'archivar'
            })
        return super(AlumnoArchivoView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.archivo = not self.object.archivo
        self.object.save()
        if self.object.archivo:
            messages.success(request, 'Se archivó al alumno satisfactoriamente')
        else:
            messages.success(request, 'Se desarchivó al alumno satisfactoriamente')
        return HttpResponseRedirect(success_url)


class ProyectoArchivoListView(ListView):
    model = Proyecto
    queryset = Proyecto.objects.filter(archivo=True)
    template_name = 'proyecto-list.html'
    paginate_by = 50
    page_kwarg = 'pagina'


    def get_context_data(self, **kwargs):
        data =  super(ProyectoArchivoListView, self).get_context_data(**kwargs)
        data.update({
            'title_page': 'Proyectos archivados'
        })
        return data


class ProyectoArchivoView(UserPassesTestMixin, DeleteView):
    model = Proyecto
    template_name = 'archivar.html'
    success_url = reverse_lazy('escuela:proyectos-list')

    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin() or self.request.user.is_supervisor() or self.request.user.is_capturista():
                return True
        return False

    def get_cancel_url(self):
        return reverse('escuela:proyectos-detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'object_type': 'proyecto',
            'cancel': self.get_cancel_url()
        })
        obj = self.get_object()
        if obj.archivo:
            kwargs.update({
                'title_page': 'Desarchivar proyecto {}'.format(self.get_object().__str__()),
                'action': 'desarchivar'
            })
        else:
            kwargs.update({
                'title_page': 'Archivar proyecto {}'.format(self.get_object().__str__()),
                'action': 'archivar'
            })
        return super(ProyectoArchivoView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.archivo = not self.object.archivo
        self.object.save()
        if self.object.archivo:
            messages.success(request, 'Se archivó el proyecto satisfactoriamente')
        else:
            messages.success(request, 'Se desarchivó el proyecto satisfactoriamente')
        return HttpResponseRedirect(success_url)

class InstitucionArchivoListView(ListView):
    model = Institucion
    queryset = Institucion.objects.filter(archivo=True)
    template_name = 'institucion-list.html'
    paginate_by = 50
    page_kwarg = 'pagina'


    def get_context_data(self, **kwargs):
        data =  super(InstitucionArchivoListView, self).get_context_data(**kwargs)
        data.update({
            'title_page': 'Instituciones archivadas'
        })
        return data


class InstitucionArchivoView(UserPassesTestMixin, DeleteView):
    model = Institucion
    template_name = 'archivar.html'
    success_url = reverse_lazy('escuela:instituciones-list')

    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin() or self.request.user.is_supervisor() or self.request.user.is_capturista():
                return True
        return False

    def get_cancel_url(self):
        return reverse('escuela:instituciones-detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'object_type': 'institución',
            'cancel': self.get_cancel_url()
        })
        obj = self.get_object()
        if obj.archivo:
            kwargs.update({
                'title_page': 'Desarchivar institucion {}'.format(self.get_object().__str__()),
                'action': 'desarchivar'
            })
        else:
            kwargs.update({
                'title_page': 'Archivar institucion {}'.format(self.get_object().__str__()),
                'action': 'archivar'
            })
        return super(InstitucionArchivoView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.archivo = not self.object.archivo
        self.object.save()
        if self.object.archivo:
            messages.success(request, 'Se archivó la institución satisfactoriamente')
        else:
            messages.success(request, 'Se desarchivó la institución satisfactoriamente')
        return HttpResponseRedirect(success_url)