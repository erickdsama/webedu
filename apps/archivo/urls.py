from django.conf.urls import url

from apps.archivo.views import AlumnoArchivoListView, AlumnoArchivoView, ProyectoArchivoListView, ProyectoArchivoView, \
    InstitucionArchivoListView, InstitucionArchivoView

urlpatterns = [
    url(r'^alumnos/$', AlumnoArchivoListView.as_view(), name='alumnos-list'),
    url(r'^alumnos/archivar/(?P<pk>\d+)/$', AlumnoArchivoView.as_view(), name='alumnos-archivar'),
    url(r'^proyectos/$', ProyectoArchivoListView.as_view(), name='proyectos-list'),
    url(r'^proyectos/archivar/(?P<pk>\d+)/$', ProyectoArchivoView.as_view(), name='proyectos-archivar'),
    url(r'^instituciones/$', InstitucionArchivoListView.as_view(), name='instituciones-list'),
    url(r'^instituciones/archivar/(?P<pk>\d+)/$', InstitucionArchivoView.as_view(), name='instituciones-archivar'),
]