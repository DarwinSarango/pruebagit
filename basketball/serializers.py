"""
Serializadores del módulo Basketball
TODO: Implementar los serializadores para cada modelo
"""

from rest_framework import serializers


# TODO: Implementar UsuarioSerializer
class UsuarioSerializer(serializers.Serializer):
    """Serializador para Usuario"""
    pass


# TODO: Implementar GrupoAtletaSerializer
class GrupoAtletaSerializer(serializers.Serializer):
    """Serializador para GrupoAtleta"""
    pass


# TODO: Implementar AtletaSerializer
class AtletaSerializer(serializers.Serializer):
    """Serializador para Atleta"""
    pass


# TODO: Implementar InscripcionSerializer
class InscripcionSerializer(serializers.Serializer):
    """Serializador para Inscripcion"""
    pass


# TODO: Implementar PruebaAntropometricaSerializer
class PruebaAntropometricaSerializer(serializers.Serializer):
    """Serializador para PruebaAntropometrica"""
    pass


# TODO: Implementar PruebaFisicaSerializer
class PruebaFisicaSerializer(serializers.Serializer):
    """Serializador para PruebaFisica"""
    pass


# TODO: Implementar EntrenadorSerializer
class EntrenadorSerializer(serializers.Serializer):
    """Serializador para Entrenador"""
    pass


# TODO: Implementar EstudianteVinculacionSerializer
class EstudianteVinculacionSerializer(serializers.Serializer):
    """Serializador para EstudianteVinculacion"""
    pass
