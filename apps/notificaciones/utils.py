from django.contrib.sites.shortcuts import get_current_site

from apps.notificaciones.models import Notificacion


def get_absolute_url(request, uri):
    site = get_current_site(request)
    return "http://{}{}".format(site.domain, uri)

def generate_notification(request, users_to_notify, url, text):
    for user in users_to_notify:
        if user is not request.user:
            notification = Notificacion.objects.create(
                usuario=user,
                url=url,
                texto=text,
                usuario_creo=request.user
            )
            # Send notification via email
            notification.send_email(request)