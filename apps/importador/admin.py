from django.contrib import admin
from apps.importador.models import Importacion, ImportacionInstituciones


class ImportacionAdmin(admin.ModelAdmin):
    list_display = ('fecha','usuario','procesado','importados_num','alumnos_creados','alumnos_actualizados')

class ImportacionInstitucionesAdmin(admin.ModelAdmin):
    list_display = ('fecha','usuario','procesado','importados_num','instituciones_creadas','instituciones_actualizadas')

admin.site.register(Importacion, ImportacionAdmin)
admin.site.register(ImportacionInstituciones, ImportacionInstitucionesAdmin)
