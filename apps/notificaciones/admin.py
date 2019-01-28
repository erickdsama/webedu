from django.contrib import admin

# Register your models here.
from apps.notificaciones.models import Notificacion

class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('fecha','usuario','texto','visto')

admin.site.register(Notificacion, NotificacionAdmin)