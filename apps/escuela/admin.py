from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.escuela.models import Alumno, InformacionPersonal, ContactoEmergencia, Periodo, Grupo, Institucion, Proyecto, DiasPracticas, \
    Supervisor, DiaClase, NotaAlumno
from apps.escuela.resources import AlumnoResource


class InformacionPersonalInline(admin.StackedInline):
    model = InformacionPersonal

class NotasInline(admin.StackedInline):
    model = NotaAlumno

class ContactoEmergenciaInline(admin.StackedInline):
    model = ContactoEmergencia

class AlumnoAdmin(ImportExportModelAdmin):
    list_display = ('__str__','matricula','email','nombre')
    inlines = (InformacionPersonalInline, ContactoEmergenciaInline, NotasInline)
    resource_class = AlumnoResource

# class DocenteAdmin(admin.ModelAdmin):
#     list_display = ('__str__','telefono','activo')

class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('ano','semestre','activo')

class DiaClaseInline(admin.StackedInline):
    model = DiaClase

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('campus','nivel','grupo','periodo','docente',)
    filter_horizontal = ('alumnos',)
    inlines = (DiaClaseInline,)
    list_filter = ('periodo',)

class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre','direccion')

class DiasPracticaInline(admin.StackedInline):
    model = DiasPracticas

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre','modalidad','institucion')
    inlines = (DiasPracticaInline,)

class NotaAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno','usuario','nota','fecha')

    def alumno(self, obj):
        return obj.alumno.nombre

    def usuario(self, obj):
        return obj.usuario.get_full_name()

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Supervisor)
admin.site.register(NotaAlumno, NotaAlumnoAdmin)