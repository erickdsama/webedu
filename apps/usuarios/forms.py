from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator

from apps.escuela.models import TURNO_CHOICES
from apps.usuarios.models import User


class LoginForm(forms.Form):
    error_css_class = 'error'
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input-sm form-control fg-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input-sm form-control fg-input'}), label='Contraseña')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if cleaned_data.get('email') and cleaned_data.get('password'):
            user = authenticate(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
            if user is None:
                raise forms.ValidationError("El usuario no es válido")
        return cleaned_data


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-lg fg-input'}), label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-lg fg-input'}), label='Repite la contraseña')
    # tipo_usuario = forms.ModelMultipleChoiceField(widget=forms.Select(choices=((grupo.pk, grupo.name) for grupo in Group.objects.all().order_by('name')), attrs={'class':'selectpicker'}))
    tipo_usuario = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))
    telefono = forms.CharField(validators=[
        RegexValidator("[0-9]{10}", "Por favor agregué un número telefónico válido", )], required=False, widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}), max_length=10)
    turno = forms.CharField(widget=forms.Select(choices=TURNO_CHOICES, attrs={'class':'selectpicker'}), required=False)
    sector = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class':'form-control input-lg fg-input'}))
    class Meta:
        model = User
        fields = ('nombre','apellido_paterno','apellido_materno','email','is_active','telefono')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'apellido_paterno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'apellido_materno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'email': forms.EmailInput(attrs={'class':'form-control input-lg fg-input'}),
        }

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password', 'Las contraseñas no coinciden')
        if cleaned_data.get('tipo_usuario'):
            if cleaned_data.get('tipo_usuario').filter(name__icontains='supervisor').exists():
                if not cleaned_data.get('telefono'):
                    self.add_error('telefono', 'Este campo es requerido')
                if not cleaned_data.get('turno'):
                    self.add_error('turno', 'Este campo es requerido')
                if not cleaned_data.get('sector'):
                    self.add_error('sector', 'Este campo es requerido')
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    # tipo_usuario = forms.CharField(
    #     widget=forms.Select(choices=((grupo.pk, grupo.name) for grupo in Group.objects.all().order_by('name')),
    #                         attrs={'class': 'selectpicker'}))
    telefono = forms.CharField(validators=[
        RegexValidator("[0-9]{10}", "Por favor agregué un número telefónico válido", )], required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-lg fg-input'}), max_length=10)
    turno = forms.CharField(widget=forms.Select(choices=TURNO_CHOICES, attrs={'class': 'selectpicker'}), required=False)
    sector = forms.CharField(max_length=15, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control input-lg fg-input'}))
    tipo_usuario = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                                  widget=forms.SelectMultiple(attrs={'class': 'selectpicker'}))
    class Meta:
        model = User
        fields = ('nombre','apellido_paterno','apellido_materno','email','is_active','telefono')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'apellido_paterno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'apellido_materno': forms.TextInput(attrs={'class':'form-control input-lg fg-input'}),
            'email': forms.EmailInput(attrs={'class':'form-control input-lg fg-input'}),
        }

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password', 'Las contraseñas no coinciden')
        if cleaned_data.get('tipo_usuario'):
            if cleaned_data.get('tipo_usuario').filter(name__icontains='supervisor').exists():
                if not cleaned_data.get('telefono'):
                    self.add_error('telefono', 'Este campo es requerido')
                if not cleaned_data.get('turno'):
                    self.add_error('turno', 'Este campo es requerido')
                if not cleaned_data.get('sector'):
                    self.add_error('sector', 'Este campo es requerido')
        return cleaned_data

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg fg-input'}),
                               label='Nueva Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg fg-input'}),
                                label='Repite la contraseña')

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password', 'Las contraseñas no coinciden')
        return cleaned_data


class ProfilePictureForm(forms.ModelForm):
    imagen = forms.ImageField()

    class Meta:
        model = User
        fields = ('imagen',)