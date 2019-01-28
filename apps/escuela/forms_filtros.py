from django import forms
from apps.escuela.models import Alumno, CAMPUS_CHOICES, Institucion, SECTOR_CHOICES, \
    NIVEL_CHOICES as NIVEL_INSTITUCION_CHOICES, SUBNIVEL_CHOICES as SUBNIVEL_INSTITUCION_CHOICES, \
    Supervisor, Periodo

NIVEL_CHOICES = (
    ('','Nivel'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
)

CAMPUS_CHOICES = (
    ('', 'Campus'),
    CAMPUS_CHOICES[0],
    CAMPUS_CHOICES[1],
)

def get_institucion_choices():
    choices = [('','Institución')]
    for institucion in Institucion.objects.all().order_by('nombre'):
        choices.append((institucion.pk, institucion.nombre))
    return choices


class AlumnoFiltrosForm(forms.Form):
    buscar = forms.CharField(label='Nombre o matrícula', required=False, widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder':'Buscar nombre, apellido, matrícula'}))
    nivel = forms.CharField(widget=forms.Select(choices=NIVEL_CHOICES, attrs={'class':'selectpicker'}), required=False)
    # activo = forms.CharField(widget=forms.Select(choices=((True,'Activo'),(False,'Inactivo')), attrs={'class':'selectpicker'}), required=False)
    campus = forms.CharField(widget=forms.Select(choices=CAMPUS_CHOICES, attrs={'class':'selectpicker'}), required=False)
    # Comentar cuando se hagan migraciones
    institucion = forms.CharField(widget=forms.Select(choices=get_institucion_choices(), attrs={'class':'selectpicker'}))

SECTOR_CHOICES_FILTRO = [
    ('','Sector'),
]
SECTOR_CHOICES_FILTRO.extend(SECTOR_CHOICES)

NIVEL_CHOICES_FILTRO = [
    ('','Nivel'),
]
NIVEL_CHOICES_FILTRO.extend(NIVEL_INSTITUCION_CHOICES)

SUBNIVEL_CHOICES_FILTRO = [
    ('','Subnivel'),
]
SUBNIVEL_CHOICES_FILTRO.extend(SUBNIVEL_INSTITUCION_CHOICES)

def get_supervisor_choices():
    choices = [('','Supervisor')]
    for supervisor in Supervisor.objects.all().order_by('usuario__nombre','usuario__apellido_paterno'):
        choices.append((supervisor.pk, supervisor.usuario.get_full_name()))
    return choices

class InstitucionFiltrosForm(forms.Form):
    buscar = forms.CharField(label='Nombre', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control input-sm', 'placeholder': 'Buscar por nombre'}))
    sector = forms.CharField(widget=forms.Select(choices=SECTOR_CHOICES_FILTRO, attrs={'class':'selectpicker'}), required=False)
    nivel = forms.CharField(widget=forms.Select(choices=NIVEL_CHOICES_FILTRO, attrs={'class':'selectpicker'}), required=False)
    subnivel = forms.CharField(widget=forms.Select(choices=SUBNIVEL_CHOICES_FILTRO, attrs={'class':'selectpicker'}), required=False)
    supervisor = forms.CharField(required=False, widget=forms.Select(attrs={'class':'selectpicker'}, choices=get_supervisor_choices()))
    nivel_practicas = forms.CharField(required=False, widget=forms.Select(attrs={'class': 'selectpicker'}, choices=(
        ('','Nivel prácticas'),
        (1,'Prácticas 1'),
        (2,'Prácticas 2'),
        (3,'Prácticas 3'),
    )))

class GrupoFiltrosForm(forms.Form):
    nivel = forms.CharField(widget=forms.Select(choices=NIVEL_CHOICES, attrs={'class': 'selectpicker'}), required=False)
    campus = forms.CharField(widget=forms.Select(choices=CAMPUS_CHOICES, attrs={'class': 'selectpicker'}),
                             required=False)
    supervisor = forms.CharField(required=False,
                                 widget=forms.Select(attrs={'class': 'selectpicker'}, choices=get_supervisor_choices()))
    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.all().order_by('-pk'),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        initial=Periodo.objects.filter(activo=True).last().pk
    )

def get_instituciones_choices():
    choices = [('','Institución')]
    choices.extend(Institucion.objects.all().order_by('nombre').values_list('pk','nombre'))
    return choices

class ProyectoFiltrosForm(forms.Form):
    buscar = forms.CharField(label='Nombre del proyecto o alumno', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control input-sm', 'placeholder': 'Buscar por nombre, alumno o matrícula'}))
    institucion = forms.CharField(required=False,
                                 widget=forms.Select(attrs={'class': 'selectpicker'}, choices=get_instituciones_choices()))