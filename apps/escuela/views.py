import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Value, Q, F, Case, When
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, DetailView, UpdateView
from django.views.generic import DeleteView

from apps.escuela.forms import AlumnoForm, DocenteCreateForm, InstitucionForm, ProyectoForm, PeriodoForm, GrupoForm, \
    ContactoEmergenciaForm, DocenteBaseForm, DiaPracticaForm, NotaForm, DiaClaseForm
from apps.escuela.forms_filtros import AlumnoFiltrosForm, InstitucionFiltrosForm, GrupoFiltrosForm, ProyectoFiltrosForm
from apps.escuela.models import Alumno, InformacionPersonal, Institucion, Proyecto, Periodo, Grupo, \
    ContactoEmergencia, DiaPractica, DiaClase, NotaAlumno, Supervisor
from apps.escuela.resources import AlumnoResource
from apps.notificaciones.utils import generate_notification
from apps.usuarios.models import User
from django.http import JsonResponse


class AlumnoListView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = 'alumno-list.html'
    ordering = ('nivel','nombre')
    paginate_by = 50
    page_kwarg = 'pagina'
    queryset = Alumno.objects.exclude(archivo=True)

    def get_queryset(self):
        # queryset = super(AlumnoListView, self).get_queryset().annotate(campus=F('grupo__campus'))
        queryset = super(AlumnoListView, self).get_queryset()
        # queryset = super(AlumnoListView, self).get_queryset().annotate(grupo_actual=Case(
        #     When(grupo__periodo__activo=True, then='grupo')
        # ))
        # queryset = super(AlumnoListView, self).get_queryset()
        filtros = self.request.GET
        if filtros.get('buscar'):
            queryset = queryset.filter(Q(nombre__unaccent__icontains=filtros.get('buscar')) | Q(matricula__icontains=filtros.get('buscar')))
        if filtros.get('nivel'):
            queryset = queryset.filter(nivel=filtros.get('nivel'))
        if filtros.get('campus'):
            queryset = queryset.filter(grupo__campus=filtros.get('campus'), grupo__periodo__activo=True)
        if filtros.get('institucion'):
            queryset = queryset.filter(proyecto__institucion__pk=filtros.get('institucion'))
        return queryset

    def get_context_data(self, **kwargs):
        data = super(AlumnoListView, self).get_context_data(**kwargs)
        # data.update({'form_filtros':AlumnoFiltrosForm(self.request.GET)})
        filtrosForm = AlumnoFiltrosForm(self.request.GET)
        data.update({'title_page': 'Lista de alumnos'})
        data.update({'filtrosForm':filtrosForm})
        data.update({'filtrosPaginacion':self.get_filtros_paginacion()})
        return data

    def get_filtros_paginacion(self):
        filtros = []
        for key, value in self.request.GET.items():
            if key != self.page_kwarg:
                filtros.append("{}={}".format(key, value))
        return '&'.join(filtros)

    def export(self):
        queryset = self.get_queryset()


        alumno_resource = AlumnoResource()
        dataset = alumno_resource.export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="alumnos.xls"'
        return response

    def get(self, request, *args, **kwargs):
        if request.GET.get('export'):
            return self.export()

        return super(AlumnoListView, self).get(request, *args, **kwargs)



class AlumnoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'alumno-create.html'
    form_class = AlumnoForm
    model = Alumno
    success_url = '/escuela/alumnos/'

    def get_context_data(self, **kwargs):
        data = super(AlumnoCreateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Agregar alumno'})
        return data

    def form_valid(self, form):
        alumno = form.save(commit=False)
        alumno.nombre = form.cleaned_data.get('nombre').upper()
        alumno.save()
        # Guardamos la informacion personal
        informacion_obj = InformacionPersonal.objects.create(alumno=alumno, telefono=form.cleaned_data.get('telefono'),telefono2=form.cleaned_data.get('telefono2'),no_servicio_medico=form.cleaned_data.get('no_servicio_medico'),tipo_seguro=form.cleaned_data.get('tipo_seguro'))
        # Notificacion
        messages.success(self.request,'Se agregó el alumno con éxito')
        return super(AlumnoCreateView, self).form_valid(form)

class AlumnoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'alumno-create.html'
    form_class = AlumnoForm
    model = Alumno
    success_url = '/escuela/alumnos/'

    def get_context_data(self, **kwargs):
        data = super(AlumnoUpdateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Editar alumno'})
        return data

    def get_initial(self):
        initial = super(AlumnoUpdateView, self).get_initial()
        alumno = self.get_object()
        try:
            informacion_personal = alumno.informacion_personal
            initial.update({
                'telefono': informacion_personal.telefono,
                'telefono2': informacion_personal.telefono2,
                'telefono2': informacion_personal.telefono2,
                'no_servicio_medico': informacion_personal.no_servicio_medico,
                'tipo_seguro': informacion_personal.tipo_seguro,
            })
        except:
            pass
        return initial

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return super(AlumnoUpdateView, self).get_success_url()

    def form_valid(self, form):
        alumno = form.save(commit=False)
        alumno.nombre = form.cleaned_data.get('nombre').upper()
        alumno.save()
        informacion_personal, new = InformacionPersonal.objects.get_or_create(alumno=self.get_object())
        informacion_personal.telefono = form.cleaned_data.get('telefono')
        informacion_personal.telefono2 = form.cleaned_data.get('telefono2')
        informacion_personal.no_servicio_medico = form.cleaned_data.get('no_servicio_medico')
        informacion_personal.tipo_seguro = form.cleaned_data.get('tipo_seguro')
        informacion_personal.save()
        # InformacionPersonal.objects.filter(alumno=self.get_object()).update(
        #     telefono=form.cleaned_data.get('telefono'),
        #     telefono2=form.cleaned_data.get('telefono2'),
        #     no_servicio_medico=form.cleaned_data.get('no_servicio_medico'),
        #     tipo_seguro=form.cleaned_data.get('tipo_seguro'),
        # )
        if form.has_changed():
            messages.success(self.request, 'Se actualizó la información del alumno con éxito')
        return super(AlumnoUpdateView, self).form_valid(form)

class AlumnoDetailView(LoginRequiredMixin, DetailView):
    model = Alumno
    template_name = 'alumno-detail.html'

    def get_context_data(self, **kwargs):
        data = super(AlumnoDetailView, self).get_context_data()
        data.update({'title_page':self.get_object().get_full_name})
        # Form contacto emergencia
        data.update({'form_contacto':self.get_form_contacto()})
        data.update({'pestana':self.kwargs.get('pestana','informacion_personal')})
        return data

    def get_form_contacto(self):
        if self.request.method == 'POST':
            form = ContactoEmergenciaForm(self.request.POST)
        else:
            form = ContactoEmergenciaForm()
        return form

    def get_form_nota(self):
        if self.request.method == 'POST':
            form = NotaForm(self.request.POST)
        else:
            form = NotaForm()
        return form

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        if self.request.POST.get('accion') == 'contactoEmergenciaAdd':
            form = self.get_form_contacto()
            if form.is_valid():
                contacto = form.save(commit=False)
                contacto.alumno = self.get_object()
                contacto.save()
                messages.success(self.request, 'Se agregó el contacto con éxito')
                return redirect(reverse('escuela:alumno-detail', args=[self.object.pk, 'contactos_emergencia']))
        elif self.request.POST.get('accion') == 'contactoEmergenciaDelete':
            contacto = ContactoEmergencia.objects.get(pk=self.request.POST.get('contacto_pk'))
            contacto.delete()
            messages.success(self.request, 'Se eliminó el contacto satisfactoriamente')
            return redirect(reverse('escuela:alumno-detail', args=[self.object.pk, 'contactos_emergencia']))
        elif self.request.POST.get('accion') == 'notaAlumnoAdd':
            form = self.get_form_nota()
            if form.is_valid():
                nota = form.save(commit=False)
                nota.usuario = self.request.user
                nota.alumno = self.get_object()
                nota.save()
        return self.render_to_response(self.get_context_data())

class AlumnoDeleteView(LoginRequiredMixin, DeleteView):
    model = Alumno
    success_url = reverse_lazy('escuela:alumnos-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'El alumno se eliminó con éxito')
        return super(AlumnoDeleteView, self).delete(request, *args, **kwargs)

class DocenteListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'docente-list.html'
    ordering = ('nombre', 'apellido_paterno', 'apellido_materno')
    queryset = User.objects.filter(groups__name__icontains='docente')

class DocenteDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'docente-detail.html'

    def get_context_data(self, **kwargs):
        data = super(DocenteDetailView, self).get_context_data(**kwargs)
        data.update({'title_page':'Docente: {}'.format(self.object.get_full_name())})
        return data

class DocenteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'docente-create.html'
    model = User
    form_class = DocenteCreateForm
    success_url = reverse_lazy('escuela:docentes-list')

    def form_valid(self, form):
        group, new = Group.objects.get_or_create(name='Docente')
        grupo_docente = Group.objects.filter(name__icontains='docente')
        # usuario, new = User.objects.get_or_create(email=form.cleaned_data.get('email'), nombre=form.cleaned_data.get('nombre'), apellido_paterno=form.cleaned_data.get('apellido_paterno'), apellido_materno=form.cleaned_data.get('apellido_materno'))
        usuario = form.save()
        usuario.groups.set(grupo_docente)
        usuario.set_password(form.cleaned_data.get('password'))
        usuario.save()
        messages.success(self.request, 'Se creó el docente con éxito')
        return super(DocenteCreateView, self).form_valid(form)

class DocenteUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = DocenteBaseForm
    template_name = 'docente-update.html'
    success_url = reverse_lazy('escuela:docentes-list')

    # def get_initial(self):
    #     initial = super(DocenteUpdateView, self).get_initial()
    #     initial.update({
    #         'nombre': self.object.usuario.nombre,
    #         'apellido_paterno': self.object.usuario.apellido_paterno,
    #         'apellido_materno': self.object.usuario.apellido_materno,
    #         'email': self.object.usuario.email,
    #     })
    #     return initial

    def get_context_data(self, **kwargs):
        data = super(DocenteUpdateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Editar Docente: {}'.format(self.object.get_full_name())})
        return data

    def form_valid(self, form):
        docente = form.save()
        # docente.usuario.nombre = form.cleaned_data.get('nombre')
        # docente.usuario.apellido_paterno = form.cleaned_data.get('apellido_paterno')
        # docente.usuario.apellido_materno = form.cleaned_data.get('apellido_materno')
        # docente.usuario.email = form.cleaned_data.get('email')
        # docente.usuario.save()
        if form.has_changed():
            messages.success(self.request, 'Se editó la información del docente satisfactoriamente')
        return super(DocenteUpdateView, self).form_valid(form)

class DocenteDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('escuela:docentes-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'El docente se eliminó con éxito')
        return super(DocenteDeleteView, self).delete(request, *args, **kwargs)


class InstitucionListView(LoginRequiredMixin, ListView):
    model = Institucion
    template_name = 'institucion-list.html'
    paginate_by = 20
    page_kwarg = 'pagina'
    ordering = ('nombre','pk')
    queryset = Institucion.objects.exclude(archivo=True)

    def get_context_data(self, **kwargs):
        data = super(InstitucionListView, self).get_context_data(**kwargs)
        data.update({'title_page':'Lista de instituciones'})
        data.update({'filtrosForm':InstitucionFiltrosForm(self.request.GET)})
        data.update({'filtrosPaginacion': self.get_filtros_paginacion()})
        return data

    def get_filtros_paginacion(self):
        filtros = []
        for key, value in self.request.GET.items():
            if key != self.page_kwarg:
                filtros.append("{}={}".format(key, value))
        return '&'.join(filtros)

    def get_queryset(self):
        queryset = super(InstitucionListView, self).get_queryset()
        filtros = self.request.GET
        if filtros.get('buscar'):
            queryset = queryset.filter(nombre__icontains=filtros.get('buscar'))
        if filtros.get('sector'):
            queryset = queryset.filter(sector=filtros.get('sector'))
        if filtros.get('nivel'):
            queryset = queryset.filter(nivel=filtros.get('nivel'))
        if filtros.get('subnivel'):
            queryset = queryset.filter(subnivel=filtros.get('subnivel'))
        if filtros.get('supervisor'):
            queryset = queryset.filter(supervisores__id=filtros.get('supervisor'))
        if filtros.get('nivel_practicas'):
            queryset =  queryset.filter(proyectos__alumnos__nivel=filtros.get('nivel_practicas')).distinct()
        return queryset


class InstitucionCreateView(LoginRequiredMixin, CreateView):
    model = Institucion
    template_name = 'institucion-form.html'
    success_url = reverse_lazy('escuela:instituciones-list')
    form_class = InstitucionForm

    def form_valid(self, form):
        messages.success(self.request, 'Se agregó la institución con éxito')
        return super(InstitucionCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(InstitucionCreateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Crear nueva Institución'})
        return data

class InstitucionDetailView(LoginRequiredMixin, DetailView):
    model = Institucion
    template_name = 'institucion-detail.html'

    def get_context_data(self, **kwargs):
        return super(InstitucionDetailView, self).get_context_data(title_page="Institución {}".format(self.object.nombre))

class InstitucionUpdateView(LoginRequiredMixin, UpdateView):
    model = Institucion
    form_class = InstitucionForm
    template_name = 'institucion-form.html'
    success_url = reverse_lazy('escuela:instituciones-list')

    def get_context_data(self, **kwargs):
        return super(InstitucionUpdateView, self).get_context_data(title_page="Institución {}".format(self.object.nombre))

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, ' Se ha actualizado la institución con éxito')
        return super(InstitucionUpdateView, self).form_valid(form)

class InstitucionDeleteView(LoginRequiredMixin, DeleteView):
    model = Institucion
    success_url = reverse_lazy('escuela:instituciones-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La institución se eliminó satisfactoriamente')
        return super(InstitucionDeleteView, self).delete(request, *args, **kwargs)

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto-list.html'
    ordering = ('nombre','pk')
    queryset = Proyecto.objects.exclude(archivo=True)

    def get_context_data(self, **kwargs):
        data = super(ProyectoListView, self).get_context_data(**kwargs)
        data.update({'title_page':'Lista de proyectos'})
        data.update({'filtrosForm': ProyectoFiltrosForm(self.request.GET)})
        return data

    def get_queryset(self):
        queryset = super(ProyectoListView, self).get_queryset()
        filtros = self.request.GET
        if filtros.get('buscar'):
            queryset = queryset.filter(Q(nombre__icontains=filtros.get('buscar')) | Q(alumnos__nombre__icontains=filtros.get('buscar')) | Q(alumnos__matricula=filtros.get('buscar')))
        if filtros.get('institucion'):
            queryset = queryset.filter(institucion__pk=filtros.get('institucion'))
        return queryset

class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    success_url = reverse_lazy('escuela:proyectos-list')
    template_name = 'proyecto-form.html'

    def get_context_data(self, **kwargs):
        data = super(ProyectoCreateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Crear nuevo proyecto'})
        data.update({'cancel_url':self.request.GET.get('next', self.success_url)})
        return data

class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto-detail.html'
    context_object_name = 'proyecto'

    def get_context_data(self, **kwargs):
        return super(ProyectoDetailView, self).get_context_data(title_page='Proyecto: {}'.format(self.object.nombre), pestana=self.kwargs.get('pestana','informacion'))

class ProyectoUpdateView(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    success_url = reverse_lazy('escuela:proyectos-list')
    template_name = 'proyecto-form.html'

    def get_success_url(self):
        return self.request.GET.get('next',self.success_url)

    def get_context_data(self, **kwargs):
        return super(ProyectoUpdateView, self).get_context_data(title_page='Editar proyecto: {}'.format(self.object.nombre), cancel_url=self.request.GET.get('next', self.success_url))

    def form_valid(self, form):
        if form.has_changed():
            messages.success(self.request, 'Se ha actualizado la información del proyecto satisfactoriamente')
        return super(ProyectoUpdateView, self).form_valid(form)

class ProyectoDeleteView(LoginRequiredMixin, DeleteView):
    model = Proyecto
    success_url = reverse_lazy('escuela:proyectos-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Se ha eliminado el proyecto con éxito')
        return super(ProyectoDeleteView, self).delete(request, *args, **kwargs)

class PeriodoListView(LoginRequiredMixin, ListView):
    model = Periodo
    template_name = 'periodo-list.html'
    ordering = ('-ano')

    def get_context_data(self, **kwargs):
        data = super(PeriodoListView, self).get_context_data(**kwargs)
        data.update({'title_page':'Periodos'})
        return data

class PeriodoCreateView(LoginRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'periodo-form.html'
    success_url = reverse_lazy('escuela:periodos-list')

    def get_context_data(self, **kwargs):
        data = super(PeriodoCreateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Agregar nuevo periodo'})
        return data

    def get_initial(self):
        initial = super(PeriodoCreateView, self).get_initial()
        initial.update({'ano':datetime.date.today().year})
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Se agregó el nuevo periodo satisfactoriamente')
        if form.cleaned_data.get('activo'):
            Periodo.objects.all().update(activo=False)
        return super(PeriodoCreateView, self).form_valid(form)

class GrupoListView(LoginRequiredMixin, ListView):
    model = Grupo
    template_name = 'grupo-list.html'

    def get_context_data(self, **kwargs):
        data = super(GrupoListView, self).get_context_data(**kwargs)
        data.update({
            'title_page':'Grupos',
            'filtrosForm':GrupoFiltrosForm(self.request.GET)
        })
        return data

    def get_queryset(self):
        queryset = super(GrupoListView, self).get_queryset()
        filtros = self.request.GET
        if filtros.get('periodo') is None:
            queryset = queryset.filter(periodo__activo=True)
        else:
            queryset = queryset.filter(periodo=filtros.get('periodo'))
        if filtros.get('campus'):
            queryset = queryset.filter(campus=filtros.get('campus'))
        if filtros.get('nivel'):
            queryset = queryset.filter(nivel=filtros.get('nivel'))
        if filtros.get('supervisor'):
            queryset = queryset.filter(supervisor__id=filtros.get('supervisor'))
        return queryset

class GrupoDetailView(LoginRequiredMixin, DetailView):
    model = Grupo
    template_name = 'grupo-detail.html'

    def get_context_data(self, **kwargs):
        data = super(GrupoDetailView, self).get_context_data(**kwargs)
        data.update({'title_page':'Detalle del grupo {}'.format(self.object.grupo)})
        return data

class GrupoCreateView(LoginRequiredMixin, CreateView):
    model = Grupo
    template_name = 'grupo-form.html'
    form_class = GrupoForm
    success_url = reverse_lazy('escuela:grupos-list')

    def form_valid(self, form):
        messages.success(self.request, ' Se creó el grupo con éxito')
        return super(GrupoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(GrupoCreateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Agregar nuevo grupo'})
        data.update({'cancel_url': self.request.GET.get('next', self.success_url)})
        return data

class GrupoUpdateView(LoginRequiredMixin, UpdateView):
    model = Grupo
    template_name = 'grupo-form.html'
    form_class = GrupoForm
    success_url = reverse_lazy('escuela:grupos-list')

    def get_context_data(self, **kwargs):
        data = super(GrupoUpdateView, self).get_context_data(**kwargs)
        data.update({'title_page':'Editar grupo'})
        data.update({'cancel_url':self.request.GET.get('next', self.success_url)})
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Se actualizó la información del grupo satisfactoriamente')
        return super(GrupoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)

class DiadeClaseView(LoginRequiredMixin, CreateView):
    model = DiaClase
    template_name = 'grupo-dia-clase.html'
    form_class = DiaClaseForm
    success_url = reverse_lazy('escuela:grupos-list')

    def get_context_data(self, **kwargs):
        data = super(DiadeClaseView, self).get_context_data(**kwargs)
        data.update({
            'title_page':'Editar horario de clase',
            'grupo':get_object_or_404(Grupo, pk=self.kwargs.get('grupo_pk'))
        })
        return data

    def form_valid(self, form):
        dia_clase = form.save(commit=False)
        dia_clase.grupo = get_object_or_404(Grupo, pk=self.kwargs.get('grupo_pk'))
        dia_clase.save()
        messages.success(self.request, 'Se agregó el día de clase con éxito')
        return super(DiadeClaseView, self).form_valid(form)

    def get_success_url(self):
        return reverse('escuela:grupos-horario', args=[self.kwargs.get('grupo_pk')])

class DiaClaseDeleteView(LoginRequiredMixin, DeleteView):
    model = DiaClase

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Se eliminó el día de clase con éxito')
        return super(DiaClaseDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('escuela:grupos-horario', args=[self.kwargs.get('grupo_pk')])


def buscador(request):
    search_list = list()
    data_resp = list()
    search = request.POST.get('busqueda')
    resultados_busqueda = list()

    # Busqueda alumnos
    alumnos = Alumno.objects.filter(Q(nombre__icontains=search) | Q(matricula=search))
    data_resp += ({
        'nombre': "{} ({})".format(alumno.nombre, alumno.matricula),
        'url': alumno.get_absolute_url(),
        'tipo': 'Alumno'
     } for alumno in alumnos)
    # Busqueda Docentes
    docentes = User.objects.annotate(nombre_completo=Concat('nombre', Value(' '), 'apellido_paterno', Value(' '), 'apellido_materno')).filter(nombre_completo__icontains=search, groups__name__icontains='docente')
    data_resp += ({
        'nombre': "{} (DOCENTE)".format(docente.nombre_completo),
        'url': docente.get_absolute_url(),
        'tipo': 'Docente'
    } for docente in docentes)
    # Busqueda de proyectos
    proyectos = Proyecto.objects.filter(Q(nombre__icontains=search) | Q(institucion__nombre__icontains=search))
    data_resp += ({
        'nombre': proyecto.nombre,
        'url': proyecto.get_absolute_url(),
        'tipo': 'Proyecto'
    } for proyecto in proyectos)
    # Busqueda de instituciones
    instituciones = Institucion.objects.filter(nombre__icontains=search)
    data_resp += ({
        'nombre': institucion.nombre,
        'url': institucion.get_absolute_url(),
        'tipo': 'Institución'
    } for institucion in instituciones)
    # Busuqeda grupos
    if 'grupo' in search.lower():
        grupos = Grupo.objects.annotate(grupo_nombre=Concat(Value('Grupo '),'nivel','grupo')).filter(periodo__activo=True, grupo_nombre__icontains=search)
        if grupos.exists():
            data_resp += ({
                'nombre': 'Grupo {}{}'.format(grupo.nivel, grupo.grupo),
                'url': grupo.get_absolute_url(),
                'tipo': 'Grupo'
            } for grupo in grupos)
    data_resp = sorted(data_resp, key=lambda k: k['nombre'])
    return JsonResponse(data_resp, safe=False)


class DiasPracticaView(CreateView):
    template_name = 'dias-practica.html'
    model = DiaPractica
    form_class = DiaPracticaForm

    def get_alumno(self):
        alumno = Alumno.objects.get(pk=self.kwargs.get('alumno_pk'))
        return alumno

    def get_context_data(self, **kwargs):
        data = super(DiasPracticaView, self).get_context_data(**kwargs)
        data.update({'alumno':self.get_alumno()})
        return data

    def form_valid(self, form):
        dia = form.save(commit=False)
        dia.alumno = self.get_alumno()
        dia.save()
        messages.success(self.request, 'Se agregó el día de práctica con éxito')
        return super(DiasPracticaView, self).form_valid(form)

    def get_success_url(self):
        return reverse('escuela:alumno-dias-practica', args=[self.get_alumno().pk])

class DiasPracticaDelete(DeleteView):
    model = DiaPractica

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Se eliminó el día de práctica con éxito')
        return super(DiasPracticaDelete, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('escuela:alumno-dias-practica', args=[self.object.alumno.pk])

class AgregarNotaView(LoginRequiredMixin, CreateView):
    model = NotaAlumno
    form_class = NotaForm
    data = None

    def form_valid(self, form):
        nota = form.save(commit=False)
        nota.usuario = self.request.user
        nota.alumno = self.get_alumno()
        nota.save()
        # Generar notificaciones
        self.send_notifications()
        return JsonResponse({'success':True, 'success_url':self.get_success_url()})

    def post(self, request, *args, **kwargs):
        dict_post = json.loads(request.body.decode('utf-8'))
        self.data = dict_post
        return super(AgregarNotaView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse({'success':False, 'errors':form.errors.as_json()})

    def get_form_kwargs(self):
        kwargs = super(AgregarNotaView, self).get_form_kwargs()
        if self.data is not None:
            kwargs.update({'data':self.data})
        return kwargs

    def get_success_url(self):
        return "{}notas".format(reverse('escuela:alumno-detail', args=[self.kwargs.get('alumno_pk')]))

    def get_alumno(self):
        return get_object_or_404(Alumno, pk=self.kwargs.get('alumno_pk'))

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def send_notifications(self):
        alumno = self.get_alumno()
        texto = "{} agregó una nota para el alumno {}".format(self.request.user.get_full_name(), alumno.get_full_name().upper())
        url = self.get_success_url()
        if alumno.get_grupo():
            docente = alumno.get_grupo().docente
        else:
            docente = False
        supervisores = alumno.get_supervisores()
        if supervisores or docente:
            if supervisores:
                if docente:
                    supervisores = User.objects.filter(Q(pk=docente.pk) | Q(supervisor__in=supervisores))
                else:
                    supervisores = User.objects.filter(supervisor__in=supervisores)
            else:
                supervisores = User.objects.filter(pk=docente.pk)
            # Generar alertas
            supervisores = supervisores.distinct()
            generate_notification(self.request, supervisores, url, texto)


class RemoveAlumnoGrupo(LoginRequiredMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
         grupo = get_object_or_404(Grupo, pk=self.kwargs.get('grupo_pk'))
         grupo.alumnos.remove(self.kwargs.get('alumno_pk'))
         success_url = self.get_success_url()
         messages.success(request,'Se removió el alumno del grupo con éxito')
         return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('escuela:grupos-detail', args=[self.kwargs.get('grupo_pk')])

class SupervisorListView(LoginRequiredMixin, ListView):
    model = Supervisor
    template_name = 'supervisor-list.html'
    ordering = ('usuario__nombre','usuario__apellido_paterno','usuario__apellido_materno')

    def get_context_data(self, **kwargs):
        data = super(SupervisorListView, self).get_context_data(**kwargs)
        data.update({'title_page':'Supervisores'})
        return data

class SupervisorDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'supervisor'
    model = Supervisor
    template_name = 'supervisor-detail.html'

    def get_context_data(self, **kwargs):
        data = super(SupervisorDetailView, self).get_context_data(**kwargs)
        data.update({
            'title_page': self.get_object().usuario.get_full_name(),
            'subtitle_page': 'Supervisor'
        })
        return data

class EliminarNotaView(LoginRequiredMixin, DeleteView):
    model = NotaAlumno

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())

    def delete(self, request, *args, **kwargs):
        nota = self.get_object()
        if request.user.is_admin() or nota.usuario == request.user:
            messages.success(request, 'Se eliminó la nota satisfactoriamente')
        else:
            messages.error(request, 'No tienes permisos para eliminar esta nota')
            return redirect(self.get_success_url())
        return super(EliminarNotaView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        nota = self.get_object()
        return reverse('escuela:alumno-detail', args=[nota.alumno.pk, 'notas'])