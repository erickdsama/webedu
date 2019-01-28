from django import forms
from django.core.validators import RegexValidator

from apps.usuarios.models import User
from .models import Alumno, InformacionPersonal, ContactoEmergencia, Institucion, Proyecto, Periodo, \
    DIAS_CHOICES, Grupo, CAMPUS_CHOICES, DiaPractica, NotaAlumno, DiaClase
from .models import TIPO_SEGURO_CHOICES, VALIDACION_TELEFONO
import datetime

# def numero_telefonico(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )

class AlumnoForm(forms.ModelForm):
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}), validators=[VALIDACION_TELEFONO], required=False, max_length=10)
    telefono2 = forms.CharField(required=False, label="Teléfono 2", widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}), validators=[VALIDACION_TELEFONO], max_length=10)
    no_servicio_medico = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}), label='Número de servicio médico')
    tipo_seguro = forms.CharField(widget=forms.Select(choices=TIPO_SEGURO_CHOICES, attrs={'class':'selectpicker'}), required=False)
    class Meta:
        model = Alumno
        fields = ("__all__")
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            # 'apellido_paterno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            # 'apellido_materno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'matricula': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'email': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'nivel': forms.Select(attrs={'class':'selectpicker'})
        }

class InformacionPersonalForm(forms.ModelForm):
    class Meta:
        model = InformacionPersonal
        exclude = ("alumno",)


class DocenteBaseForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre(s)', widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}))
    apellido_paterno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}))
    apellido_materno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control input-lg fg-input'}))
    class Meta:
        model = User
        fields = ('nombre','apellido_paterno','apellido_materno','email','telefono','is_active')
        widgets = {
            'telefono':forms.TextInput(attrs={'class':'form-control input-lg fg-input'})
        }

class DocenteCreateForm(DocenteBaseForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control input-lg fg-input'}))
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput(attrs={'class':'form-control input-lg fg-input'}))

    def clean(self):
        cleaned_data = super(DocenteCreateForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password', 'Las contraseñas no coinciden')
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', 'Este email ya se encuentra registrado')
        return cleaned_data


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ('nombre','direccion','referencia','telefono','contacto_directo','contacto_directo_email','responsable_principal','nivel','subnivel','ambito','sector','supervisores','status')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'direccion': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'referencia': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'telefono': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'contacto_directo': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'contacto_directo_email': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'responsable_principal': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'nivel': forms.Select(attrs={'class':'selectpicker'}),
            'subnivel': forms.Select(attrs={'class':'selectpicker'}),
            'ambito': forms.Select(attrs={'class':'selectpicker'}),
            'sector': forms.Select(attrs={'class': 'selectpicker'}),
            'supervisores': forms.SelectMultiple(attrs={'class': 'selectpicker'})
        }

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre','modalidad','institucion','espacio','alumnos','tipo','beneficiarios','beneficiarios_cantidad','actividades',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'espacio': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'beneficiarios': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'beneficiarios_cantidad': forms.NumberInput(attrs={'class':'form-control input-lg fg-input'}),
            'actividades': forms.Textarea(attrs={'class':'form-control input-lg fg-input','rows':'3'}),
            'modalidad': forms.Select(attrs={'class':'selectpicker'}),
            'institucion': forms.Select(attrs={'class':'selectpicker'}),
            'tipo': forms.Select(attrs={'class':'selectpicker'}),
            'alumnos':forms.SelectMultiple(attrs={'class':'selectpicker','data-live-search':'true'})
        }

def get_ano_choices():
    year = datetime.date.today().year
    return ((y,y) for y in range(year-5,year+5))

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ('ano','semestre','activo')
        widgets = {
            'ano': forms.Select(choices=get_ano_choices(), attrs={'class':'selectpicker'},),
            'semestre': forms.Select(attrs={'class':'selectpicker'}),
        }

class GrupoForm(forms.ModelForm):
    # dias = forms.MultipleChoiceField(choices=DIAS_CHOICES, widget=forms.Select(attrs={'class':'selectpicker','multiple':'multiple'}))
    # horario = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Grupo
        fields = ('periodo','campus','nivel','docente','grupo','alumnos','supervisor')
        widgets = {
            'periodo': forms.Select(attrs={'class':'selectpicker'}),
            'campus': forms.Select(attrs={'class':'selectpicker'}),
            'nivel': forms.Select(attrs={'class':'selectpicker'}),
            'docente': forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}),
            'supervisor': forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'}),
            'grupo': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'alumnos': forms.SelectMultiple(attrs={'class':'selectpicker', 'data-live-search':'true'}),
        }

class ContactoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ('nombre','telefono','direccion')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'telefono': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'direccion': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
        }

class DiaPracticaForm(forms.ModelForm):
    class Meta:
        model = DiaPractica
        fields = ('dia','hora_inicio', 'hora_fin')
        widgets = {
            'dia': forms.Select(attrs={'class':'selectpicker'}),
            'hora_inicio': forms.TimeInput(attrs={'class':'time-picker form-control','placeholder':'01:00'}),
            'hora_fin': forms.TimeInput(attrs={'class':'time-picker form-control','placeholder':'16:00'}),
        }

class DiaClaseForm(forms.ModelForm):
    class Meta:
        model = DiaClase
        fields = ('dia','hora_inicio','hora_fin')
        widgets = {
            'dia': forms.Select(attrs={'class': 'selectpicker'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'time-picker form-control', 'placeholder': '01:00'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'time-picker form-control', 'placeholder': '16:00'}),
        }

class NotaForm(forms.ModelForm):
    class Meta:
        model = NotaAlumno
        fields = ('nota',)