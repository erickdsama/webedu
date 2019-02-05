from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Length
from django.urls import reverse

VALIDACION_TELEFONO = RegexValidator("[0-9]{7,10}","Por favor agregué un número telefónico válido",)

ALUMNO_NIVEL_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','Termino'),
)
STATUS_CHOICES = (
    ('Activo','Activo'),
    ('Inactivo','Inactivo')
)
class Alumno(models.Model):
    class Meta:
        verbose_name = 'alumno'
        verbose_name_plural = 'alumnos'

    nombre = models.CharField(max_length=65, verbose_name='Nombre(s)')
    # apellido_paterno = models.CharField(max_length=25)
    # apellido_materno = models.CharField(max_length=25, blank=True, null=True)
    matricula = models.CharField(max_length=10, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    nivel = models.CharField(max_length=1, choices=ALUMNO_NIVEL_CHOICES, default='1')
    activo = models.BooleanField(default=True)
    archivo = models.BooleanField(default=False)

    def get_name_display(self):
        return self.__str__()

    def get_full_name(self):
        return self.nombre

    def __str__(self):
        return "{} ({})".format(self.nombre, self.matricula)

    def get_grupo(self):
        if self.grupo_set.filter(periodo__activo=True).exists():
            return self.grupo_set.filter(periodo__activo=True).first()
        return False

    def get_absolute_url(self):
        return reverse('escuela:alumno-detail', args=[self.pk])

    def get_supervisores(self):
        if self.dias_practica.exists() and self.proyecto_set.exists():
            proyecto = self.proyecto_set.last()
            supervisores = Supervisor.objects.filter(institucion=proyecto.institucion)
            # Fin de semana
            if self.dias_practica.filter(Q(dia__iexact='sabado') | Q(dia__iexact='domingo')).exists():
                return supervisores.filter(turno='Fin de semana')
            # Entre semana
            else:
                # Matutino
                if self.dias_practica.filter(hora_inicio__hour__gte=6, hora_inicio__hour__lt=14).exists():
                    return supervisores.filter(turno='Matutino')
                # Vespertino
                else:
                    return supervisores.filter(turno='Vespertino')
        return False

TIPO_SEGURO_CHOICES = (
    ('Facultativo','Facultativo'),
    ('ICHISAL','ICHISAL'),
    ('IMSS','IMSS'),
    ('ISSSTE','ISSSTE'),
    ('Pensiones','Pensiones'),
    ('Privado','Privado'),
    ('Seguro popular','Seguro popular'),
    ('Otro','Otro'),
)
class InformacionPersonal(models.Model):
    class Meta:
        verbose_name = 'información personal'
        verbose_name_plural = 'informacion personal'

    alumno = models.OneToOneField(Alumno, related_name='informacion_personal')
    telefono = models.CharField(max_length=10, validators=[VALIDACION_TELEFONO], blank=True, null=True)
    telefono2 = models.CharField(max_length=10, blank=True, null=True, validators=[VALIDACION_TELEFONO])
    no_servicio_medico = models.CharField(max_length=45, blank=True, null=True)
    tipo_seguro = models.CharField(max_length=15, choices=TIPO_SEGURO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.alumno.__str__()

class ContactoEmergencia(models.Model):
    class Meta:
        verbose_name = 'Contacto emergencia'
        verbose_name_plural = 'Contactos emergencia'

    alumno = models.ForeignKey(Alumno, related_name='contactos_emergencia')
    nombre = models.CharField(max_length=55)
    telefono = models.CharField(max_length=10, validators=[VALIDACION_TELEFONO])
    direccion = models.CharField(max_length=140, blank=True, null=True)

    def __str__(self):
        return self.nombre

DIAS_CHOICES = (
    ('Lunes','Lunes'),
    ('Martes','Martes'),
    ('Miercoles','Miércoles'),
    ('Jueves','Jueves'),
    ('Viernes','Viernes'),
    ('Sabado','Sabado'),
    ('Domingo','Domingo'),
)
class DiaPractica(models.Model):
    class Meta:
        verbose_name = 'Día de práctica'
        verbose_name_plural = 'Días de práctica'

    alumno = models.ForeignKey(Alumno, related_name='dias_practica')
    dia = models.CharField(max_length=11, choices=DIAS_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return "{} {}-{}".format(self.dia, self.hora_inicio, self.hora_fin)

# class Docente(models.Model):
#     class Meta:
#         verbose_name = 'Docente'
#         verbose_name_plural = 'Docentes'
#
#     usuario = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)
#     telefono = models.CharField(max_length=10, validators=[VALIDACION_TELEFONO])
#     activo = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.usuario.__str__()
#
#     def get_full_name(self):
#         return "{} {} {}".format(self.usuario.nombre, self.usuario.apellido_paterno, self.usuario.apellido_materno)
#
#     def get_absolute_url(self):
#         return reverse('escuela:docente-detail', args=[self.pk])

TURNO_CHOICES = (
    ('Matutino','Matutino'),
    ('Vespertino','Vespertino'),
    ('Fin de semana','Fin de semana')
)
class Supervisor(models.Model):
    class Meta:
        verbose_name = 'Supervisor'
        verbose_name_plural = 'Supervisores'

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    telefono = models.CharField(max_length=10, validators=[
        RegexValidator("[0-9]{10}", "Por favor agregué un número telefónico válido", )])
    turno = models.CharField(max_length=15, choices=TURNO_CHOICES)
    sector = models.CharField(max_length=45)

    def __str__(self):
        return self.usuario.__str__()

    def get_alumnos(self):
        if self.turno == 'Matutino':
            return Alumno.objects.exclude(archivo=True).filter(
                proyecto__institucion__in=self.institucion_set.all(),
                dias_practica__dia__in=['Lunes','Martes','Miercoles','Jueves','Viernes'],
                dias_practica__hora_inicio__hour__gte=6,
                dias_practica__hora_inicio__hour__lt=14,
            ).distinct()
        elif self.turno == 'Vespertino':
            return Alumno.objects.exclude(archivo=True).filter(
                proyecto__institucion__in=self.institucion_set.all(),
                dias_practica__dia__in=['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'],
                dias_practica__hora_inicio__hour__gte=14,
                dias_practica__hora_inicio__hour__lt=22,
            ).distinct()
        elif self.turno == 'Fin de semana':
            return Alumno.objects.exclude(archivo=True).filter(
                proyecto__institucion__in=self.institucion_set.all(),
                dias_practica__dia__in=['Sabado', 'Domingo'],
            ).distinct()
        else:
            return []

    def grupos_periodo(self):
        return self.grupos.filter(periodo__activo=True)

    def get_instituciones(self):
        """ Retorna las instituciones ligadas al supervisor que no se encuentran archivadas """
        return self.institucion_set.exclude(archivo=True)


SEMESTRE_CHOICES = (
    ('1','Enero-Junio'),
    ('2','Agosto-Diciembre')
)

class Periodo(models.Model):
    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'

    ano = models.CharField(max_length=4, verbose_name="Año")
    semestre = models.CharField(max_length=1, choices=SEMESTRE_CHOICES)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}".format(self.ano, self.semestre)

CAMPUS_CHOICES = (
    ('ICSA','ICSA'),
    ('CU','CU')
)
NIVEL_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
)
class Grupo(models.Model):
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    campus = models.CharField(max_length=4, choices=CAMPUS_CHOICES)
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES)
    grupo = models.CharField(max_length=1)
    periodo = models.ForeignKey(Periodo, related_name='grupos')
    docente = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='grupos', blank=True, null=True, limit_choices_to={'groups__name__icontains':'docente'}, on_delete=models.SET_NULL)
    supervisor = models.ForeignKey(Supervisor, related_name='grupos', blank=True, null=True, on_delete=models.SET_NULL)
    # horario = models.TextField()
    alumnos = models.ManyToManyField(Alumno, blank=True)

    def __str__(self):
        return self.grupo

    def get_absolute_url(self):
        return reverse('escuela:grupos-detail', args=[self.pk])

    def get_alumnos(self):
        alumnos = self.alumnos.all().annotate(matricula_length=Length('matricula'))
        return alumnos.order_by('matricula_length','matricula')

NIVEL_CHOICES = (
    ('Inicial','Inicial'),
    ('Básico','Básico'),
    ('Medio Superior','Medio Superior'),
    ('Superior','Superior'),
)
SUBNIVEL_CHOICES = (
    ('Preescolar','Preescolar'),
    ('Primaria','Primaria'),
    ('Secundaria','Secundaria'),
    ('Formación técnica','Formación técnica'),
    ('Bachillerato','Bachillerato'),
    ('Pregrado','Pregrado'),
    ('Posgrado','Posgrado')
)
AMBITO_CHOICES = (
    ('Docencia', 'Docencia'),
    ('Educación Comunitaria', 'Educación Comunitaria'),
    ('Educación Especial', 'Educación Especial'),
    ('Capacitación Industrial y Empresarial', 'Capacitación Industrial y Empresarial'),
    ('Gestión Educativa', 'Gestión Educativa'),
    ('Investigación Educativa', 'Investigación Educativa'),
    ('Gestión Cultural', 'Gestión Cultural'),
)
SECTOR_CHOICES = (
    ('Privado','Privado'),
    ('Público','Público'),
)

class Institucion(models.Model):
    class Meta:
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'

    nombre = models.CharField(max_length=85)
    direccion = models.CharField(max_length=140)
    referencia = models.CharField(max_length=140, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True, validators=[VALIDACION_TELEFONO])
    contacto_directo = models.CharField(max_length=55, blank=True, null=True)
    contacto_directo_email = models.EmailField(blank=True, null=True)
    responsable_principal = models.CharField(max_length=85, blank=True, null=True)
    nivel = models.CharField(max_length=14, blank=True, null=True, choices=NIVEL_CHOICES)
    subnivel = models.CharField(max_length=18, blank=True, null=True, choices=SUBNIVEL_CHOICES)
    ambito = models.CharField(max_length=45, choices=AMBITO_CHOICES)
    sector = models.CharField(max_length=10, choices=SECTOR_CHOICES)
    supervisores = models.ManyToManyField(Supervisor, blank=True)
    status = models.BooleanField(default=True)
    archivo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('escuela:instituciones-detail', args=[self.pk])

MODALIDAD_CHOICES = (
    ('Desarrollo de trayectos profesionales','Desarrollo de trayectos profesionales'),
    ('Emprendimiento','Emprendimiento'),
    ('Estadías Docentes','Estadías Docentes'),
    ('Independiente','Independiente'),
    ('Intervención Educativa','Intervención Educativa'),
    ('Proyecto Independiente','Proyecto Independiente'),
)

TIPO_CHOICES = (
    ('Equipo','Equipo'),
    ('Individual','Individual'),
)

class Proyecto(models.Model):
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    nombre = models.CharField(max_length=140)
    modalidad = models.CharField(max_length=37, choices=MODALIDAD_CHOICES, blank=True, null=True)
    institucion = models.ForeignKey(Institucion, related_name='proyectos')
    espacio = models.CharField(max_length=55, blank=True, null=True)
    alumnos = models.ManyToManyField(Alumno, blank=True
                                     )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo del proyecto')
    # informacion respecto a la practica
    beneficiarios = models.CharField(max_length=140, help_text='Categoría', blank=True, null=True)
    beneficiarios_cantidad = models.PositiveIntegerField(blank=True, null=True)
    actividades = models.CharField(max_length=255, blank=True, null=True, verbose_name='Actividades que realiza')
    archivo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('escuela:proyectos-detail', args=[self.pk])

class DiasPracticas(models.Model):
    class Meta:
        verbose_name = 'Día de práctica'
        verbose_name_plural = 'Días de práctica'

    proyecto = models.ForeignKey(Proyecto, related_name='dias')
    dia = models.CharField(max_length=11, choices=DIAS_CHOICES)
    hora = models.TimeField()

    def __str__(self):
        return "{} {}".format(self.dia, self.hora)


class DiaClase(models.Model):
    class Meta:
        verbose_name = 'Día de clase'
        verbose_name_plural = 'Días de clase'

    grupo = models.ForeignKey(Grupo, related_name='dias')
    dia = models.CharField(max_length=11, choices=DIAS_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return "{} {}-{}".format(self.dia, self.hora_inicio, self.hora_fin)


class NotaAlumno(models.Model):
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    fecha = models.DateTimeField(auto_now_add=True)
    alumno =models.ForeignKey(Alumno, related_name='notas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notas')
    nota = models.TextField()

    def __str__(self):
        return "{}: {}".format(self.usuario.get_full_name(), self.nota)


