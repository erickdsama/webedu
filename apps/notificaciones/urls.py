from django.conf.urls import url

from apps.notificaciones.views import MisNotificacionesListView, NotificacionRedirectView

urlpatterns = [
    url(r'^mis-notificaciones/$', MisNotificacionesListView.as_view(), name='mis-notificaciones'),
    url(r'^ver-notificacion/(?P<pk>\d+)/$', NotificacionRedirectView.as_view(), name='ver-notificacion'),
]