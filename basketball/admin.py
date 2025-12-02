"""
Configuración del Admin de Django para el módulo Basketball
"""

from django.contrib import admin
from basketball.models import (
    Usuario, GrupoAtleta, Entrenador, EstudianteVinculacion,
    Atleta, Inscripcion, PruebaAntropometrica, PruebaFisica
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'email', 'dni', 'rol', 'estado', 'fecha_registro']
    list_filter = ['rol', 'estado', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'email', 'dni']
    ordering = ['-fecha_registro']


@admin.register(GrupoAtleta)
class GrupoAtletaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'categoria', 'rango_edad_minima', 'rango_edad_maxima', 'estado', 'fecha_creacion']
    list_filter = ['categoria', 'estado', 'fecha_creacion']
    search_fields = ['nombre', 'categoria']
    ordering = ['nombre']


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_usuario_nombre', 'especialidad', 'club_asignado']
    list_filter = ['especialidad', 'club_asignado']
    search_fields = ['usuario__nombre', 'usuario__apellido', 'especialidad', 'club_asignado']
    
    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"
    get_usuario_nombre.short_description = 'Usuario'


@admin.register(EstudianteVinculacion)
class EstudianteVinculacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_usuario_nombre', 'carrera', 'semestre']
    list_filter = ['carrera', 'semestre']
    search_fields = ['usuario__nombre', 'usuario__apellido', 'carrera']
    
    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"
    get_usuario_nombre.short_description = 'Usuario'


@admin.register(Atleta)
class AtletaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_atleta', 'apellido_atleta', 'dni', 'edad', 'sexo', 'grupo', 'estado']
    list_filter = ['sexo', 'grupo', 'estado', 'tipo_sangre']
    search_fields = ['nombre_atleta', 'apellido_atleta', 'dni', 'email']
    ordering = ['apellido_atleta', 'nombre_atleta']
    date_hierarchy = 'fecha_nacimiento'


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['id', 'atleta', 'fecha_inscripcion', 'tipo_inscripcion', 'habilitada', 'fecha_creacion']
    list_filter = ['tipo_inscripcion', 'habilitada', 'fecha_inscripcion', 'fecha_creacion']
    search_fields = ['atleta__nombre_atleta', 'atleta__apellido_atleta', 'atleta__dni']
    ordering = ['-fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'


@admin.register(PruebaAntropometrica)
class PruebaAntropometricaAdmin(admin.ModelAdmin):
    list_display = ['id', 'atleta', 'fecha_registro', 'estatura', 'peso', 'indice_masa_corporal', 'estado']
    list_filter = ['estado', 'fecha_registro']
    search_fields = ['atleta__nombre_atleta', 'atleta__apellido_atleta', 'atleta__dni']
    ordering = ['-fecha_registro']
    date_hierarchy = 'fecha_registro'
    readonly_fields = ['indice_masa_corporal', 'indice_cornico']


@admin.register(PruebaFisica)
class PruebaFisicaAdmin(admin.ModelAdmin):
    list_display = ['id', 'atleta', 'fecha_registro', 'tipo_prueba', 'resultado', 'unidad_medida', 'estado']
    list_filter = ['tipo_prueba', 'estado', 'fecha_registro']
    search_fields = ['atleta__nombre_atleta', 'atleta__apellido_atleta', 'atleta__dni']
    ordering = ['-fecha_registro']
    date_hierarchy = 'fecha_registro'
