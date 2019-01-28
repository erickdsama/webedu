"""practicas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from apps.escuela import urls as escuela_urls
from apps.usuarios import urls as usuarios_urls
from apps.importador import urls as importador_urls
from apps.notificaciones import urls as notificaciones_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/escuela/alumnos/'), name='home'),
    url(r'^escuela/', include(escuela_urls, namespace='escuela', app_name='escuela')),
    url(r'^usuarios/', include(usuarios_urls, namespace='usuarios', app_name='usuarios')),
    url(r'^importador/', include(importador_urls, namespace='importador', app_name='importador')),
    url(r'^notificaciones/', include(notificaciones_urls, namespace='notificaciones', app_name='notificaciones')),
    url(r'^archivo/', include('apps.archivo.urls', namespace='archivo', app_name='archivo')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
