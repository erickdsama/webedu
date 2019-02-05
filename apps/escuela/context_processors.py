from django.urls import reverse
from django.core.urlresolvers import resolve

from apps.escuela.models import Periodo


def menu(request):
    menu = [
        {
            'nombre':'Inicio',
            'url':reverse('home'),
            'icono':'zmdi-home',
            'urls_active':[reverse('home'),]
        },
        {
            'nombre':'Alumnos',
            'url':reverse('escuela:alumnos-list'),
            'urls_active':[
                'alumnos-list',
                'alumno-create',
                'alumno-update',
                'alumno-detail',
                'alumno-dias-practica',
            ]
        },
        {
            'nombre':'Docentes',
            'url': reverse('escuela:docentes-list'),
            'urls_active': [
                'docentes-list',
                'docentes-create',
                'docente-detail',
                'docente-update',
            ]
        },
        {
            'nombre':'Instituciones',
            'url': reverse('escuela:instituciones-list'),
            'urls_active': [
                'instituciones-list',
                'instituciones-create',
                'instituciones-detail',
                'instituciones-update',
            ]
        },
        {
            'nombre':'Proyectos',
            'url': reverse('escuela:proyectos-list'),
            'urls_active': [
                'proyectos-list',
                'proyectos-create',
                'proyectos-detail',
                'proyectos-update',
            ]
        },
        {
            'nombre':'Usuarios',
            'url': reverse('usuarios:user-list'),
            'urls_active': [
                'user-list',
                'user-create',
                'user-update',
                'user-set-password',
                'user-change-password',
            ],
            'usuarios_permitidos': ['Administrador','Capturista']
        },
        {
            'nombre':'Periodos',
            'url': reverse('escuela:periodos-list'),
            'urls_active': [
                'periodos-list',
                'periodos-create',
            ],
            'usuarios_permitidos': ['Administrador']
        },
        {
            'nombre':'Grupos',
            'url': reverse('escuela:grupos-list'),
            'urls_active': [
                'grupos-list',
                'grupos-create',
                'grupos-detail',
                'grupos-update',
            ]
        },
        {
            'nombre':'Importador',
            'url': reverse('importador:importar-archivo'),
            'urls_active': [
                'importar-archivo',
                'procesar-importacion',
            ],
            'usuarios_permitidos': ['Administrador','Capturista','Supervisor']
        },
        {
            'nombre': 'Supervisores',
            'url': reverse('escuela:supervisor-list'),
            'urls_active': [
                'supervisor-list',
                'supervisor-detail',
            ]
        },
    ]
    current_url = resolve(request.path_info).url_name

    for item in menu:
        item.update({'active':current_url in item.get('urls_active')})

    return {'menu':menu}


def periodo(request):
    periodos = Periodo.objects.all()
    return {"periodos": periodos}
