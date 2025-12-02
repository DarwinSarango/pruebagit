"""
URLs del módulo Basketball
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from basketball.views import (
    AtletaViewSet, GrupoAtletaViewSet, InscripcionViewSet,
    PruebaAntropometricaViewSet, PruebaFisicaViewSet,
    EntrenadorViewSet, EstudianteVinculacionViewSet
)

# Crear el router
router = DefaultRouter()

# Registrar los ViewSets
router.register(r'atletas', AtletaViewSet, basename='atleta')
router.register(r'grupos', GrupoAtletaViewSet, basename='grupo-atleta')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'pruebas-antropometricas', PruebaAntropometricaViewSet, basename='prueba-antropometrica')
router.register(r'pruebas-fisicas', PruebaFisicaViewSet, basename='prueba-fisica')
router.register(r'entrenadores', EntrenadorViewSet, basename='entrenador')
router.register(r'estudiantes-vinculacion', EstudianteVinculacionViewSet, basename='estudiante-vinculacion')

urlpatterns = [
    path('', include(router.urls)),
]
