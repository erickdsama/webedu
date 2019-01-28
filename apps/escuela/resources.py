from import_export import resources

from apps.escuela.models import Alumno


class AlumnoResource(resources.ModelResource):
    campus = resources.Field()
    grupo = resources.Field()
    proyecto = resources.Field()
    institucion = resources.Field()

    class Meta:
        model = Alumno
        fields = (
            'matricula',
            'nombre',
            'email',
            'campus',
            'nivel',
            'grupo',
            'proyecto',
            'institucion'
        )
        export_order = (
            'matricula',
            'nombre',
            'email',
            'campus',
            'nivel',
            'grupo',
            'proyecto',
            'institucion'
        )

    def dehydrate_campus(self, obj):
        grupo = obj.get_grupo()
        if grupo:
            return grupo.campus
        else:
            return "N/A"

    def dehydrate_grupo(self, obj):
        grupo = obj.get_grupo()
        if grupo:
            return "{}-{}".format(grupo.nivel, grupo.grupo)
        else:
            return "N/A"

    def dehydrate_proyecto(self, obj):
        proyecto = obj.proyecto_set.last()
        if proyecto:
            return proyecto.nombre
        else:
            return "N/A"

    def dehydrate_institucion(self, obj):
        proyecto = obj.proyecto_set.last()
        if proyecto:
            return proyecto.institucion.nombre
        else:
            return "N/A"