from django.conf.urls import url
from django.views.generic import TemplateView

from apps.usuarios.views import LoginView, UserListView, UserCreateView, UserSetPassword, ChangePasswordView, \
    UserUpdateView, UserDeleteView, UserChangePicture
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    url(r'^iniciar-sesion/$', LoginView.as_view(), name='login'),
    url(r'logout/$', logout_then_login, name='logout'),
    url(r'^$', UserListView.as_view(), name='user-list'),
    url(r'^crear-usuario/$', UserCreateView.as_view(), name='user-create'),
    url(r'^editar-usuario/(?P<user_pk>\d+)/$', UserUpdateView.as_view(), name='user-update'),
    url(r'^eliminar-usuario/(?P<user_pk>\d+)/$', UserDeleteView.as_view(), name='user-delete'),
    url(r'^user-set-password/(?P<user_pk>\d+)/$', UserSetPassword.as_view(), name='user-set-password'),
    url(r'^cambiar-password/$', ChangePasswordView.as_view(), name='user-change-password'),
    url(r'^cambiar-imagen-perfil/$', UserChangePicture.as_view(), name='user-change-picture'),
]