"""
Vistas del módulo Basketball
TODO: Implementar las vistas/viewsets para cada recurso
"""

from rest_framework import viewsets, status
from rest_framework.response import Response


# TODO: Implementar AtletaViewSet
class AtletaViewSet(viewsets.ViewSet):
    """ViewSet para Atleta"""
    pass


# TODO: Implementar GrupoAtletaViewSet
class GrupoAtletaViewSet(viewsets.ViewSet):
    """ViewSet para GrupoAtleta"""
    pass


# TODO: Implementar InscripcionViewSet
class InscripcionViewSet(viewsets.ViewSet):
    """ViewSet para Inscripcion"""
    pass


# TODO: Implementar PruebaAntropometricaViewSet
class PruebaAntropometricaViewSet(viewsets.ViewSet):
    """ViewSet para PruebaAntropometrica"""
    pass


# TODO: Implementar PruebaFisicaViewSet
class PruebaFisicaViewSet(viewsets.ViewSet):
    """ViewSet para PruebaFisica"""
    pass


# TODO: Implementar EntrenadorViewSet
class EntrenadorViewSet(viewsets.ViewSet):
    """ViewSet para Entrenador"""
    pass


# TODO: Implementar EstudianteVinculacionViewSet
class EstudianteVinculacionViewSet(viewsets.ViewSet):
    """ViewSet para EstudianteVinculacion"""
    pass
