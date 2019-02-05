from django.conf.urls import url

from apps.escuela.views import AlumnoListView, AlumnoCreateView, DocenteListView, DocenteCreateView, \
    InstitucionListView, InstitucionCreateView, \
    ProyectoCreateView, ProyectoListView, PeriodoListView, PeriodoCreateView, GrupoListView, GrupoCreateView, \
    GrupoUpdateView, AlumnoUpdateView, AlumnoDetailView, AlumnoDeleteView, DocenteDetailView, DocenteUpdateView, \
    DocenteDeleteView, InstitucionDetailView, InstitucionUpdateView, InstitucionDeleteView, ProyectoDetailView, \
    ProyectoUpdateView, ProyectoDeleteView, DiasPracticaView, DiasPracticaDelete, GrupoDetailView, DiadeClaseView, \
    DiaClaseDeleteView, AgregarNotaView, RemoveAlumnoGrupo, SupervisorListView, SupervisorDetailView, EliminarNotaView, \
    PeriodooUpdateView

from apps.escuela.views import buscador

urlpatterns = [
    # Alumnos
    url(r'^alumnos', AlumnoListView.as_view(), name='alumnos-list'),
    url(r'^agregar-alumno/$', AlumnoCreateView.as_view(), name='alumno-create'),
    url(r'^editar-alumno/(?P<pk>\d+)/$', AlumnoUpdateView.as_view(), name='alumno-update'),
    url(r'^ver-alumno/(?P<pk>\d+)/$', AlumnoDetailView.as_view(), name='alumno-detail'),
    url(r'^ver-alumno/(?P<pk>\d+)/(?P<pestana>\w+)/$', AlumnoDetailView.as_view(), name='alumno-detail'),
    url(r'^eliminar-alumno/(?P<pk>\d+)/$', AlumnoDeleteView.as_view(), name='alumno-delete'),
    url(r'^dias-practica/(?P<alumno_pk>\d+)/$', DiasPracticaView.as_view(), name='alumno-dias-practica'),
    url(r'^dias-practica-eliminar/(?P<pk>\d+)/$', DiasPracticaDelete.as_view(), name='alumno-dias-practica-delete'),
    url(r'^agregar-nota/(?P<alumno_pk>\d+)/$', AgregarNotaView.as_view(), name='alumno-agregar-nota'),
    url(r'^eliminar-nota/(?P<pk>\d+)/$', EliminarNotaView.as_view(), name='alumno-eliminar-nota'),

#     Docentes
    url(r'^docentes/', DocenteListView.as_view(), name='docentes-list'),
    url(r'^agregar-docente/', DocenteCreateView.as_view(), name='docentes-create'),
    url(r'^ver-docente/(?P<pk>\d+)/$', DocenteDetailView.as_view(), name='docente-detail'),
    url(r'^editar-docente/(?P<pk>\d+)/$', DocenteUpdateView.as_view(), name='docente-update'),
    url(r'^eliminar-docente/(?P<pk>\d+)/$', DocenteDeleteView.as_view(), name='docente-delete'),


#     Instituciones
    url(r'^instituciones/', InstitucionListView.as_view(), name='instituciones-list'),
    url(r'^agregar-institucion/', InstitucionCreateView.as_view(), name='instituciones-create'),
    url(r'^ver-institucion/(?P<pk>\d+)/$', InstitucionDetailView.as_view(), name='instituciones-detail'),
    url(r'^editar-institucion/(?P<pk>\d+)/$', InstitucionUpdateView.as_view(), name='instituciones-update'),
    url(r'^eliminar-institucion/(?P<pk>\d+)/$', InstitucionDeleteView.as_view(), name='instituciones-delete'),

#   Proyectos
    url(r'^proyectos/', ProyectoListView.as_view(), name='proyectos-list'),
    url(r'^agregar-proyecto/', ProyectoCreateView.as_view(), name='proyectos-create'),
    url(r'^ver-proyecto/(?P<pk>\d+)/$', ProyectoDetailView.as_view(), name='proyectos-detail'),
    url(r'^editar-proyecto/(?P<pk>\d+)/$', ProyectoUpdateView.as_view(), name='proyectos-update'),
    url(r'^eliminar-proyecto/(?P<pk>\d+)/$', ProyectoDeleteView.as_view(), name='proyectos-delete'),

#     Periodos
    url(r'^periodos/', PeriodoListView.as_view(), name='periodos-list'),
    url(r'^agregar-periodo/', PeriodoCreateView.as_view(), name='periodos-create'),
    url(r'^cambiar-periodo/', PeriodooUpdateView.as_view(), name='periodos-cambiar'),
#     Grupos
    url(r'^grupos/', GrupoListView.as_view(), name='grupos-list'),
    url(r'^ver-grupo/(?P<pk>\d+)/', GrupoDetailView.as_view(), name='grupos-detail'),
    url(r'^agregar-grupo/', GrupoCreateView.as_view(), name='grupos-create'),
    url(r'^editar-grupo/(?P<pk>\d+)/', GrupoUpdateView.as_view(), name='grupos-update'),
    url(r'^horario-grupo/(?P<grupo_pk>\d+)/', DiadeClaseView.as_view(), name='grupos-horario'),
    url(r'^eliminar-horario-grupo/(?P<grupo_pk>\d+)/(?P<pk>\d+)/', DiaClaseDeleteView.as_view(), name='grupos-horario-delete'),
    url(r'^remover-alumno-grupo/(?P<grupo_pk>\d+)/(?P<alumno_pk>\d+)/', RemoveAlumnoGrupo.as_view(), name='remover-alumno-grupo'),
#   Supervisores
    url(r'^supervisores/$', SupervisorListView.as_view(), name='supervisor-list'),
    url(r'^supervisores/(?P<pk>\d+)/$', SupervisorDetailView.as_view(), name='supervisor-detail'),


#     Buscador
    url(r'buscador/$', buscador, name='buscador'),
]