"""
Serializers del módulo Basketball
"""

from rest_framework import serializers
from basketball.models import (
    Usuario, GrupoAtleta, Entrenador, EstudianteVinculacion,
    Atleta, Inscripcion, PruebaAntropometrica, PruebaFisica
)


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para Usuario"""
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'apellido', 'email', 'foto_perfil',
            'dni', 'rol', 'estado', 'fecha_registro'
        ]
        read_only_fields = ['id', 'fecha_registro']
        extra_kwargs = {
            'clave': {'write_only': True}
        }


class GrupoAtletaSerializer(serializers.ModelSerializer):
    """Serializer para GrupoAtleta"""
    cantidad_atletas = serializers.SerializerMethodField()
    
    class Meta:
        model = GrupoAtleta
        fields = [
            'id', 'nombre', 'rango_edad_minima', 'rango_edad_maxima',
            'categoria', 'fecha_creacion', 'estado', 'cantidad_atletas'
        ]
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_cantidad_atletas(self, obj):
        return obj.atletas.filter(estado=True).count()


class AtletaSerializer(serializers.ModelSerializer):
    """Serializer para Atleta"""
    grupo_nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    
    class Meta:
        model = Atleta
        fields = [
            'id', 'nombre_atleta', 'apellido_atleta', 'dni',
            'fecha_nacimiento', 'edad', 'sexo', 'email', 'telefono',
            'tipo_sangre', 'datos_representante', 'telefono_representante',
            'grupo', 'grupo_nombre', 'estado'
        ]
        read_only_fields = ['id', 'edad']


class AtletaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear Atleta"""
    
    class Meta:
        model = Atleta
        fields = [
            'nombre_atleta', 'apellido_atleta', 'dni',
            'fecha_nacimiento', 'sexo', 'email', 'telefono',
            'tipo_sangre', 'datos_representante', 'telefono_representante',
            'grupo'
        ]


class InscripcionSerializer(serializers.ModelSerializer):
    """Serializer para Inscripción"""
    atleta_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Inscripcion
        fields = [
            'id', 'atleta', 'atleta_nombre', 'fecha_inscripcion',
            'tipo_inscripcion', 'fecha_creacion', 'habilitada'
        ]
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_atleta_nombre(self, obj):
        return f"{obj.atleta.nombre_atleta} {obj.atleta.apellido_atleta}"


class PruebaAntropometricaSerializer(serializers.ModelSerializer):
    """Serializer para PruebaAntropometrica"""
    atleta_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = PruebaAntropometrica
        fields = [
            'id', 'atleta', 'atleta_nombre', 'fecha_registro',
            'indice_masa_corporal', 'estatura', 'altura_sentado',
            'envergadura', 'indice_cornico', 'peso', 'observaciones', 'estado'
        ]
        read_only_fields = ['id', 'fecha_registro', 'indice_masa_corporal', 'indice_cornico']
    
    def get_atleta_nombre(self, obj):
        return f"{obj.atleta.nombre_atleta} {obj.atleta.apellido_atleta}"


class PruebaFisicaSerializer(serializers.ModelSerializer):
    """Serializer para PruebaFisica"""
    atleta_nombre = serializers.SerializerMethodField()
    tipo_prueba_display = serializers.CharField(source='get_tipo_prueba_display', read_only=True)
    
    class Meta:
        model = PruebaFisica
        fields = [
            'id', 'atleta', 'atleta_nombre', 'fecha_registro',
            'tipo_prueba', 'tipo_prueba_display', 'resultado',
            'unidad_medida', 'observaciones', 'estado'
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def get_atleta_nombre(self, obj):
        return f"{obj.atleta.nombre_atleta} {obj.atleta.apellido_atleta}"


class EntrenadorSerializer(serializers.ModelSerializer):
    """Serializer para Entrenador"""
    usuario_nombre = serializers.SerializerMethodField()
    grupos_asignados = GrupoAtletaSerializer(source='grupos', many=True, read_only=True)
    
    class Meta:
        model = Entrenador
        fields = [
            'id', 'usuario', 'usuario_nombre', 'especialidad',
            'club_asignado', 'grupos', 'grupos_asignados'
        ]
        read_only_fields = ['id']
    
    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"


class EstudianteVinculacionSerializer(serializers.ModelSerializer):
    """Serializer para EstudianteVinculacion"""
    usuario_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = EstudianteVinculacion
        fields = [
            'id', 'usuario', 'usuario_nombre', 'carrera', 'semestre'
        ]
        read_only_fields = ['id']
    
    def get_usuario_nombre(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellido}"


# Serializers para reportes y estadísticas

class EstadisticasAtletaSerializer(serializers.Serializer):
    """Serializer para estadísticas de atleta"""
    atleta_id = serializers.IntegerField()
    atleta_nombre = serializers.CharField()
    total_pruebas_antropometricas = serializers.IntegerField()
    total_pruebas_fisicas = serializers.IntegerField()
    ultima_prueba_antropometrica = PruebaAntropometricaSerializer(allow_null=True)
    estadisticas_fisicas = serializers.DictField()


class ComparacionPruebasSerializer(serializers.Serializer):
    """Serializer para comparación de pruebas"""
    prueba_1 = serializers.DictField()
    prueba_2 = serializers.DictField()
    diferencias = serializers.DictField()
