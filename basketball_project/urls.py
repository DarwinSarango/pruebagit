"""
URL configuration for basketball_project project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Basketball Module API",
        default_version='v1',
        description="API REST para el módulo de Basketball - Gestión de atletas, grupos, inscripciones, pruebas antropométricas, pruebas físicas, entrenadores y estudiantes de vinculación.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@basketball.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


@api_view(['GET'])
def api_root(request):
    """Vista raíz de la API"""
    return Response({
        "status": "success",
        "message": "Bienvenido a la API del Módulo de Basketball",
        "version": "1.0.0",
        "endpoints": {
            "atletas": "/api/v1/atletas/",
            "grupos": "/api/v1/grupos/",
            "inscripciones": "/api/v1/inscripciones/",
            "pruebas_antropometricas": "/api/v1/pruebas-antropometricas/",
            "pruebas_fisicas": "/api/v1/pruebas-fisicas/",
            "entrenadores": "/api/v1/entrenadores/",
            "estudiantes_vinculacion": "/api/v1/estudiantes-vinculacion/",
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """Vista para verificar el estado del servicio"""
    return Response({
        "status": "healthy",
        "service": "Basketball Module API",
        "version": "1.0.0"
    }, status=status.HTTP_200_OK)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('basketball.urls')),
    path('api/', api_root, name='api-root'),
    path('health/', health_check, name='health-check'),
    # Documentación Swagger/OpenAPI
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
