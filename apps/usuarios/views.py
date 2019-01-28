from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView

from django.views.generic import FormView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from apps.escuela.models import Supervisor
from apps.usuarios.models import User
from .forms import LoginForm, UserCreateForm, PasswordForm, UserUpdateForm, ProfilePictureForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = "/escuela/alumnos"

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
        if user is not None:
            login(self.request, user)
        return super(LoginView, self).form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    ordering = ('nombre', 'apellido_paterno', 'apellido_materno')
    template_name = 'user-list.html'

    def get_context_data(self, **kwargs):
        data = super(UserListView, self).get_context_data(**kwargs)
        data.update({'title_page':'Lista de usuarios'})
        return data


class UserCreateView(FormView):
    model = User
    form_class = UserCreateForm
    template_name = 'user-create.html'
    success_url = reverse_lazy('usuarios:user-list')

    def get_context_data(self, **kwargs):
        data = super(UserCreateView, self).get_context_data(**kwargs)
        grupo_supervisor = Group.objects.filter(name__icontains='supervisor')
        if grupo_supervisor.exists():
            data.update({'supervisor_group':grupo_supervisor.first().pk})
        data.update({'title_page':'Agregar Usuario'})
        return data

    def form_valid(self, form):
        user = User.objects.create(email=form.cleaned_data.get('email'),
                                   nombre=form.cleaned_data.get('nombre'),
                                   apellido_paterno=form.cleaned_data.get('apellido_paterno'),
                                   apellido_materno=form.cleaned_data.get('apellido_materno'))
        user.set_password(form.cleaned_data.get('password'))
        if form.cleaned_data.get('tipo_usuario') == '1':
            user.is_superuser = True
            user.is_staff = True
        user.save()
        grupos = form.cleaned_data.get('tipo_usuario')
        user.groups.set(grupos)
        supervisor = Group.objects.filter(name__iexact='supervisor').first()
        if supervisor in grupos:
            supervisor = Supervisor.objects.create(usuario=user,
                                                   telefono=form.cleaned_data.get('telefono'),
                                                   turno=form.cleaned_data.get('turno'),
                                                   sector=form.cleaned_data.get('sector'))
        messages.success(self.request, 'Se creó el usuario con éxito')
        return super(UserCreateView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user-update.html'
    form_class = UserUpdateForm
    model = User
    pk_url_kwarg = 'user_pk'
    success_url = reverse_lazy('usuarios:user-list')

    def get_context_data(self, **kwargs):
        data = super(UserUpdateView, self).get_context_data(**kwargs)
        grupo_supervisor = Group.objects.filter(name__icontains='supervisor')
        if grupo_supervisor.exists():
            data.update({'supervisor_group': grupo_supervisor.first().pk})
        return data

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        usr = self.get_object()
        if usr.groups.first() is not None:
            initial.update({'tipo_usuario':usr.groups.values_list('pk', flat=True)})
        try:
            supervisor = usr.supervisor
        except:
            supervisor = False

        if supervisor:
            initial.update({
                'telefono': supervisor.telefono,
                'sector': supervisor.sector,
                'turno': supervisor.turno,
            })

        return initial

    def form_valid(self, form):
        user_obj = self.get_object()
        # user_obj.groups.clear()
        user_obj.groups.set(form.cleaned_data.get('tipo_usuario'))
        if user_obj.groups.filter(name__iexact='supervisor').exists():
            try:
                supervisor = user_obj.supervisor
            except:
                supervisor = Supervisor(usuario=user_obj)
            supervisor.telefono = form.cleaned_data.get('telefono')
            supervisor.sector = form.cleaned_data.get('sector')
            supervisor.turno = form.cleaned_data.get('turno')
            supervisor.save()
        messages.success(self.request, 'Se actualizó la información del usuario con éxito')
        return super(UserUpdateView, self).form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('usuarios:user-list')
    pk_url_kwarg = 'user_pk'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Se eliminó el usuario con éxito')
        return super(UserDeleteView, self).delete(request, *args, **kwargs)



class UserSetPassword(LoginRequiredMixin, FormView):
    form_class = PasswordForm
    template_name = 'user-set-password.html'

    def get_context_data(self, **kwargs):
        data = super(UserSetPassword, self).get_context_data(**kwargs)
        data.update({'title_page':'Cambiar contraseña de {}'.format(get_object_or_404(User, pk=self.kwargs.get('user_pk')).get_full_name())})
        if self.request.GET.get('next'):
            data.update({'cancel_url': self.request.GET.get('next')})
        else:
            data.update({'cancel_url': reverse('usuarios:user-list')})
        return data

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs.get('user_pk'))
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        messages.success(self.request, 'Se cambió la contraseña del usuario correctamente')
        return super(UserSetPassword, self).form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse('usuarios:user-list')

class ChangePasswordView(LoginRequiredMixin, FormView):
    form_class = PasswordForm
    template_name = 'user-set-password.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(ChangePasswordView, self).get_context_data(**kwargs)
        data.update({'title_page':'Cambiar mi contraseña'})
        data.update({'cancel_url':'/'})
        return data

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data.get('password'))
        self.request.user.save()
        messages.success(self.request, 'Se cambió la contraseña correctamente, inicia sesión con la nueva contraseña')
        return super(ChangePasswordView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user-detail.html'

    def get_context_data(self, **kwargs):
        return super(UserDetailView, self).get_context_data(title_page=self.get_object().get_full_name)


class UserChangePicture(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfilePictureForm
    template_name = 'user-change-profile-picture.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super(UserChangePicture, self).get_context_data(**kwargs)
        data.update({
            'title_page':'Cambiar imagen de perfil',
        })
        return data

    def form_valid(self, form):
        messages.success(self.request, 'Se cambió tu imagen de perfil con éxito')
        return super(UserChangePicture, self).form_valid(form)
