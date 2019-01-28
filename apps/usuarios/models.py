from django.db import models
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import AbstractUser

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Debe contener un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)



from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    nombre = models.CharField(max_length=25)
    apellido_paterno = models.CharField(max_length=25)
    apellido_materno = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    imagen = models.ImageField(upload_to='users/profile-pictures/', blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        if self.nombre:
            return "{} {} {}".format(self.nombre, self.apellido_paterno, self.apellido_materno)
        return self.email

    def get_full_name(self):
        return "{} {} {}".format(self.nombre, self.apellido_paterno, self.apellido_materno)

    def get_short_name(self):
        return self.email

    def get_image(self):
        if self.imagen:
            return self.imagen.url
        else:
            return '/media/avatar-default1.jpg'


def is_admin(self):
    return self.groups.filter(name__iexact='administrador').exists()

User.add_to_class('is_admin', is_admin)

def is_supervisor(self):
    return self.groups.filter(name__iexact='supervisor').exists()

User.add_to_class('is_supervisor', is_supervisor)

def is_docente(self):
    return self.groups.filter(name__iexact='docente').exists()

User.add_to_class('is_docente', is_docente)

def is_capturista(self):
    return self.groups.filter(name__iexact='capturista').exists()

User.add_to_class('is_capturista', is_capturista)

def is_visitante(self):
    return self.groups.filter(name__iexact='visitante').exists()

User.add_to_class('is_visitante', is_visitante)

def is_invitado(self):
    return self.groups.filter(name__iexact='invitado').exists()

User.add_to_class('is_invitado', is_invitado)