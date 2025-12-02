"""
Views del módulo Basketball
Implementación de vistas basadas en clases usando ViewSets
Con documentación Swagger mejorada
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from basketball.models import (
    Usuario, GrupoAtleta, Entrenador, EstudianteVinculacion,
    Atleta, Inscripcion, PruebaAntropometrica, PruebaFisica
)
from basketball.serializers import (
    UsuarioSerializer, GrupoAtletaSerializer, EntrenadorSerializer,
    EstudianteVinculacionSerializer, AtletaSerializer, AtletaCreateSerializer,
    InscripcionSerializer, PruebaAntropometricaSerializer, PruebaFisicaSerializer
)
from basketball.services.api_response import APIResponse
from basketball.services.atleta_service import AtletaService
from basketball.services.grupo_atleta_service import GrupoAtletaService
from basketball.services.inscripcion_service import InscripcionService
from basketball.services.prueba_antropometrica_service import PruebaAntropometricaService
from basketball.services.prueba_fisica_service import PruebaFisicaService
from basketball.services.entrenador_service import EntrenadorService
from basketball.services.estudiante_vinculacion_service import EstudianteVinculacionService


class AtletaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Atletas.
    
    Permite listar, crear, actualizar y eliminar atletas.
    El listado soporta filtros opcionales por query params.
    """
    
    @swagger_auto_schema(
        operation_description="Listar atletas con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('activos', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, 
                            description="Filtrar solo activos (default: true)"),
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por nombre"),
            openapi.Parameter('apellido', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por apellido"),
            openapi.Parameter('grupo_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Filtrar por grupo"),
            openapi.Parameter('sexo', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por sexo"),
            openapi.Parameter('edad_min', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Edad mínima"),
            openapi.Parameter('edad_max', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Edad máxima"),
        ],
        responses={200: AtletaSerializer(many=True)}
    )
    def list(self, request):
        """Listar atletas con filtros opcionales via query params"""
        # Verificar si hay criterios de búsqueda
        criterios = {
            'nombre': request.query_params.get('nombre'),
            'apellido': request.query_params.get('apellido'),
            'grupo_id': request.query_params.get('grupo_id'),
            'sexo': request.query_params.get('sexo'),
            'edad_min': request.query_params.get('edad_min'),
            'edad_max': request.query_params.get('edad_max'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return AtletaService.buscar_atletas(criterios)
        
        activos_solo = request.query_params.get('activos', 'true').lower() == 'true'
        return AtletaService.listar_atletas(activos_solo)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo atleta",
        request_body=AtletaCreateSerializer,
        responses={201: AtletaSerializer}
    )
    def create(self, request):
        """Crear un nuevo atleta"""
        return AtletaService.crear_atleta(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener un atleta por ID",
        responses={200: AtletaSerializer, 404: "Atleta no encontrado"}
    )
    def retrieve(self, request, pk=None):
        """Obtener un atleta por ID"""
        return AtletaService.obtener_atleta(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar un atleta completamente",
        request_body=AtletaCreateSerializer,
        responses={200: AtletaSerializer, 404: "Atleta no encontrado"}
    )
    def update(self, request, pk=None):
        """Actualizar un atleta"""
        return AtletaService.actualizar_atleta(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un atleta",
        request_body=AtletaCreateSerializer,
        responses={200: AtletaSerializer, 404: "Atleta no encontrado"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente un atleta"""
        return AtletaService.actualizar_atleta(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar un atleta (soft delete por defecto)",
        manual_parameters=[
            openapi.Parameter('soft', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Soft delete (default: true)")
        ],
        responses={200: "Atleta eliminado", 404: "Atleta no encontrado"}
    )
    def destroy(self, request, pk=None):
        """Eliminar un atleta"""
        soft_delete = request.query_params.get('soft', 'true').lower() == 'true'
        return AtletaService.eliminar_atleta(int(pk), soft_delete)
    
    @swagger_auto_schema(
        operation_description="Obtener atleta por DNI",
        responses={200: AtletaSerializer, 404: "Atleta no encontrado"}
    )
    @action(detail=False, methods=['get'], url_path='dni/(?P<dni>[^/.]+)')
    def por_dni(self, request, dni=None):
        """Obtener atleta por DNI"""
        return AtletaService.obtener_atleta_por_dni(dni)
    
    @swagger_auto_schema(
        operation_description="Asignar atleta a un grupo",
        responses={200: AtletaSerializer, 404: "Atleta o grupo no encontrado"}
    )
    @action(detail=True, methods=['post'], url_path='asignar-grupo/(?P<grupo_id>[^/.]+)')
    def asignar_grupo(self, request, pk=None, grupo_id=None):
        """Asignar atleta a un grupo"""
        return AtletaService.asignar_grupo(int(pk), int(grupo_id))


class GrupoAtletaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Grupos de Atletas.
    
    Permite listar, crear, actualizar y eliminar grupos.
    """
    
    @swagger_auto_schema(
        operation_description="Listar grupos con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('activos', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Filtrar solo activos (default: true)"),
            openapi.Parameter('categoria', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por categoría"),
        ],
        responses={200: GrupoAtletaSerializer(many=True)}
    )
    def list(self, request):
        """Listar grupos con filtros opcionales"""
        categoria = request.query_params.get('categoria')
        if categoria:
            return GrupoAtletaService.buscar_grupos_por_categoria(categoria)
        
        activos_solo = request.query_params.get('activos', 'true').lower() == 'true'
        return GrupoAtletaService.listar_grupos(activos_solo)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo grupo",
        request_body=GrupoAtletaSerializer,
        responses={201: GrupoAtletaSerializer}
    )
    def create(self, request):
        """Crear un nuevo grupo"""
        return GrupoAtletaService.crear_grupo(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener un grupo por ID",
        responses={200: GrupoAtletaSerializer, 404: "Grupo no encontrado"}
    )
    def retrieve(self, request, pk=None):
        """Obtener un grupo por ID"""
        return GrupoAtletaService.obtener_grupo(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar un grupo completamente",
        request_body=GrupoAtletaSerializer,
        responses={200: GrupoAtletaSerializer, 404: "Grupo no encontrado"}
    )
    def update(self, request, pk=None):
        """Actualizar un grupo"""
        return GrupoAtletaService.actualizar_grupo(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un grupo",
        request_body=GrupoAtletaSerializer,
        responses={200: GrupoAtletaSerializer, 404: "Grupo no encontrado"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente un grupo"""
        return GrupoAtletaService.actualizar_grupo(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar un grupo",
        manual_parameters=[
            openapi.Parameter('soft', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Soft delete (default: true)")
        ],
        responses={200: "Grupo eliminado", 404: "Grupo no encontrado"}
    )
    def destroy(self, request, pk=None):
        """Eliminar un grupo"""
        soft_delete = request.query_params.get('soft', 'true').lower() == 'true'
        return GrupoAtletaService.eliminar_grupo(int(pk), soft_delete)
    
    @swagger_auto_schema(
        operation_description="Obtener atletas de un grupo",
        responses={200: AtletaSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='atletas')
    def atletas(self, request, pk=None):
        """Obtener atletas de un grupo"""
        return GrupoAtletaService.obtener_atletas_grupo(int(pk))
    
    @swagger_auto_schema(
        operation_description="Agregar un atleta a un grupo",
        responses={200: "Atleta agregado", 400: "Error al agregar"}
    )
    @action(detail=True, methods=['post'], url_path='agregar-atleta/(?P<atleta_id>[^/.]+)')
    def agregar_atleta(self, request, pk=None, atleta_id=None):
        """Agregar atleta a un grupo"""
        return GrupoAtletaService.agregar_atleta_grupo(int(pk), int(atleta_id))
    
    @swagger_auto_schema(
        operation_description="Remover un atleta de su grupo actual",
        responses={200: "Atleta removido", 404: "Atleta no encontrado"}
    )
    @action(detail=False, methods=['post'], url_path='remover-atleta/(?P<atleta_id>[^/.]+)')
    def remover_atleta(self, request, atleta_id=None):
        """Remover atleta de su grupo"""
        return GrupoAtletaService.remover_atleta_grupo(int(atleta_id))


class InscripcionViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Inscripciones.
    """
    
    @swagger_auto_schema(
        operation_description="Listar inscripciones con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('habilitada', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Filtrar por estado habilitada"),
            openapi.Parameter('tipo', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por tipo de inscripción"),
            openapi.Parameter('atleta_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Filtrar por atleta"),
            openapi.Parameter('fecha_desde', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha desde (YYYY-MM-DD)"),
            openapi.Parameter('fecha_hasta', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha hasta (YYYY-MM-DD)"),
        ],
        responses={200: InscripcionSerializer(many=True)}
    )
    def list(self, request):
        """Listar inscripciones con filtros opcionales"""
        # Verificar filtros específicos
        habilitada = request.query_params.get('habilitada')
        if habilitada is not None:
            if habilitada.lower() == 'true':
                return InscripcionService.listar_inscripciones_habilitadas()
            elif habilitada.lower() == 'false':
                return InscripcionService.listar_inscripciones_pendientes()
        
        # Buscar por criterios si hay parámetros
        criterios = {
            'tipo_inscripcion': request.query_params.get('tipo'),
            'fecha_desde': request.query_params.get('fecha_desde'),
            'fecha_hasta': request.query_params.get('fecha_hasta'),
            'atleta_id': request.query_params.get('atleta_id'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return InscripcionService.buscar_inscripciones(criterios)
        
        return InscripcionService.listar_inscripciones()
    
    @swagger_auto_schema(
        operation_description="Crear una nueva inscripción",
        request_body=InscripcionSerializer,
        responses={201: InscripcionSerializer}
    )
    def create(self, request):
        """Crear una nueva inscripción"""
        return InscripcionService.crear_inscripcion(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener una inscripción por ID",
        responses={200: InscripcionSerializer, 404: "Inscripción no encontrada"}
    )
    def retrieve(self, request, pk=None):
        """Obtener una inscripción por ID"""
        return InscripcionService.obtener_inscripcion(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar una inscripción",
        request_body=InscripcionSerializer,
        responses={200: InscripcionSerializer, 404: "Inscripción no encontrada"}
    )
    def update(self, request, pk=None):
        """Actualizar una inscripción"""
        return InscripcionService.actualizar_inscripcion(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una inscripción",
        request_body=InscripcionSerializer,
        responses={200: InscripcionSerializer, 404: "Inscripción no encontrada"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente una inscripción"""
        return InscripcionService.actualizar_inscripcion(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar una inscripción",
        responses={200: "Inscripción eliminada", 404: "Inscripción no encontrada"}
    )
    def destroy(self, request, pk=None):
        """Eliminar una inscripción"""
        return InscripcionService.eliminar_inscripcion(int(pk))
    
    @swagger_auto_schema(
        operation_description="Habilitar una inscripción",
        responses={200: InscripcionSerializer, 404: "Inscripción no encontrada"}
    )
    @action(detail=True, methods=['post'], url_path='habilitar')
    def habilitar(self, request, pk=None):
        """Habilitar una inscripción"""
        return InscripcionService.habilitar_inscripcion(int(pk))
    
    @swagger_auto_schema(
        operation_description="Deshabilitar una inscripción",
        responses={200: InscripcionSerializer, 404: "Inscripción no encontrada"}
    )
    @action(detail=True, methods=['post'], url_path='deshabilitar')
    def deshabilitar(self, request, pk=None):
        """Deshabilitar una inscripción"""
        return InscripcionService.deshabilitar_inscripcion(int(pk))
    
    @swagger_auto_schema(
        operation_description="Obtener inscripciones de un atleta específico",
        responses={200: InscripcionSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)')
    def por_atleta(self, request, atleta_id=None):
        """Obtener inscripciones de un atleta"""
        return InscripcionService.obtener_inscripciones_atleta(int(atleta_id))


class PruebaAntropometricaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Pruebas Antropométricas.
    """
    
    @swagger_auto_schema(
        operation_description="Listar pruebas antropométricas con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('activas', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Filtrar solo activas (default: true)"),
            openapi.Parameter('atleta_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Filtrar por atleta"),
            openapi.Parameter('fecha_desde', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha desde (YYYY-MM-DD)"),
            openapi.Parameter('fecha_hasta', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha hasta (YYYY-MM-DD)"),
            openapi.Parameter('imc_min', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                            description="IMC mínimo"),
            openapi.Parameter('imc_max', openapi.IN_QUERY, type=openapi.TYPE_NUMBER,
                            description="IMC máximo"),
        ],
        responses={200: PruebaAntropometricaSerializer(many=True)}
    )
    def list(self, request):
        """Listar pruebas antropométricas con filtros opcionales"""
        criterios = {
            'atleta_id': request.query_params.get('atleta_id'),
            'fecha_desde': request.query_params.get('fecha_desde'),
            'fecha_hasta': request.query_params.get('fecha_hasta'),
            'imc_min': request.query_params.get('imc_min'),
            'imc_max': request.query_params.get('imc_max'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return PruebaAntropometricaService.buscar_pruebas(criterios)
        
        activas_solo = request.query_params.get('activas', 'true').lower() == 'true'
        return PruebaAntropometricaService.listar_pruebas(activas_solo)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva prueba antropométrica",
        request_body=PruebaAntropometricaSerializer,
        responses={201: PruebaAntropometricaSerializer}
    )
    def create(self, request):
        """Crear una nueva prueba"""
        return PruebaAntropometricaService.crear_prueba(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener una prueba antropométrica por ID",
        responses={200: PruebaAntropometricaSerializer, 404: "Prueba no encontrada"}
    )
    def retrieve(self, request, pk=None):
        """Obtener una prueba por ID"""
        return PruebaAntropometricaService.obtener_prueba(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar una prueba antropométrica",
        request_body=PruebaAntropometricaSerializer,
        responses={200: PruebaAntropometricaSerializer, 404: "Prueba no encontrada"}
    )
    def update(self, request, pk=None):
        """Actualizar una prueba"""
        return PruebaAntropometricaService.actualizar_prueba(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una prueba antropométrica",
        request_body=PruebaAntropometricaSerializer,
        responses={200: PruebaAntropometricaSerializer, 404: "Prueba no encontrada"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente una prueba"""
        return PruebaAntropometricaService.actualizar_prueba(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar una prueba antropométrica",
        manual_parameters=[
            openapi.Parameter('soft', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Soft delete (default: true)")
        ],
        responses={200: "Prueba eliminada", 404: "Prueba no encontrada"}
    )
    def destroy(self, request, pk=None):
        """Eliminar una prueba"""
        soft_delete = request.query_params.get('soft', 'true').lower() == 'true'
        return PruebaAntropometricaService.eliminar_prueba(int(pk), soft_delete)
    
    @swagger_auto_schema(
        operation_description="Obtener pruebas de un atleta",
        responses={200: PruebaAntropometricaSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)')
    def por_atleta(self, request, atleta_id=None):
        """Obtener pruebas de un atleta"""
        return PruebaAntropometricaService.obtener_pruebas_atleta(int(atleta_id))
    
    @swagger_auto_schema(
        operation_description="Obtener la última prueba de un atleta",
        responses={200: PruebaAntropometricaSerializer, 404: "No hay pruebas"}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)/ultima')
    def ultima_atleta(self, request, atleta_id=None):
        """Obtener la última prueba de un atleta"""
        return PruebaAntropometricaService.obtener_ultima_prueba_atleta(int(atleta_id))
    
    @swagger_auto_schema(
        operation_description="Comparar dos pruebas antropométricas",
        responses={200: "Resultado de comparación"}
    )
    @action(detail=False, methods=['get'], url_path='comparar/(?P<prueba_id_1>[^/.]+)/(?P<prueba_id_2>[^/.]+)')
    def comparar(self, request, prueba_id_1=None, prueba_id_2=None):
        """Comparar dos pruebas"""
        return PruebaAntropometricaService.comparar_pruebas(int(prueba_id_1), int(prueba_id_2))


class PruebaFisicaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Pruebas Físicas.
    """
    
    @swagger_auto_schema(
        operation_description="Listar pruebas físicas con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('activas', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Filtrar solo activas (default: true)"),
            openapi.Parameter('atleta_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Filtrar por atleta"),
            openapi.Parameter('tipo', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por tipo de prueba"),
            openapi.Parameter('fecha_desde', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha desde (YYYY-MM-DD)"),
            openapi.Parameter('fecha_hasta', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Fecha hasta (YYYY-MM-DD)"),
        ],
        responses={200: PruebaFisicaSerializer(many=True)}
    )
    def list(self, request):
        """Listar pruebas físicas con filtros opcionales"""
        criterios = {
            'atleta_id': request.query_params.get('atleta_id'),
            'tipo_prueba': request.query_params.get('tipo'),
            'fecha_desde': request.query_params.get('fecha_desde'),
            'fecha_hasta': request.query_params.get('fecha_hasta'),
            'resultado_min': request.query_params.get('resultado_min'),
            'resultado_max': request.query_params.get('resultado_max'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return PruebaFisicaService.buscar_pruebas(criterios)
        
        activas_solo = request.query_params.get('activas', 'true').lower() == 'true'
        return PruebaFisicaService.listar_pruebas(activas_solo)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva prueba física",
        request_body=PruebaFisicaSerializer,
        responses={201: PruebaFisicaSerializer}
    )
    def create(self, request):
        """Crear una nueva prueba"""
        return PruebaFisicaService.crear_prueba(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener una prueba física por ID",
        responses={200: PruebaFisicaSerializer, 404: "Prueba no encontrada"}
    )
    def retrieve(self, request, pk=None):
        """Obtener una prueba por ID"""
        return PruebaFisicaService.obtener_prueba(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar una prueba física",
        request_body=PruebaFisicaSerializer,
        responses={200: PruebaFisicaSerializer, 404: "Prueba no encontrada"}
    )
    def update(self, request, pk=None):
        """Actualizar una prueba"""
        return PruebaFisicaService.actualizar_prueba(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una prueba física",
        request_body=PruebaFisicaSerializer,
        responses={200: PruebaFisicaSerializer, 404: "Prueba no encontrada"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente una prueba"""
        return PruebaFisicaService.actualizar_prueba(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar una prueba física",
        manual_parameters=[
            openapi.Parameter('soft', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN,
                            description="Soft delete (default: true)")
        ],
        responses={200: "Prueba eliminada", 404: "Prueba no encontrada"}
    )
    def destroy(self, request, pk=None):
        """Eliminar una prueba"""
        soft_delete = request.query_params.get('soft', 'true').lower() == 'true'
        return PruebaFisicaService.eliminar_prueba(int(pk), soft_delete)
    
    @swagger_auto_schema(
        operation_description="Obtener tipos de prueba física disponibles",
        responses={200: "Lista de tipos"}
    )
    @action(detail=False, methods=['get'], url_path='tipos')
    def tipos(self, request):
        """Obtener tipos de prueba disponibles"""
        return PruebaFisicaService.obtener_tipos_prueba()
    
    @swagger_auto_schema(
        operation_description="Obtener pruebas de un atleta",
        responses={200: PruebaFisicaSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)')
    def por_atleta(self, request, atleta_id=None):
        """Obtener pruebas de un atleta"""
        return PruebaFisicaService.obtener_pruebas_atleta(int(atleta_id))
    
    @swagger_auto_schema(
        operation_description="Obtener pruebas de un atleta filtradas por tipo",
        responses={200: PruebaFisicaSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)/tipo/(?P<tipo_prueba>[^/.]+)')
    def por_tipo(self, request, atleta_id=None, tipo_prueba=None):
        """Obtener pruebas de un atleta por tipo"""
        return PruebaFisicaService.obtener_pruebas_por_tipo(int(atleta_id), tipo_prueba)
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas de pruebas de un atleta",
        responses={200: "Estadísticas"}
    )
    @action(detail=False, methods=['get'], url_path='atleta/(?P<atleta_id>[^/.]+)/estadisticas')
    def estadisticas(self, request, atleta_id=None):
        """Obtener estadísticas de un atleta"""
        return PruebaFisicaService.obtener_estadisticas_atleta(int(atleta_id))
    
    @swagger_auto_schema(
        operation_description="Comparar dos pruebas físicas",
        responses={200: "Resultado de comparación"}
    )
    @action(detail=False, methods=['get'], url_path='comparar/(?P<prueba_id_1>[^/.]+)/(?P<prueba_id_2>[^/.]+)')
    def comparar(self, request, prueba_id_1=None, prueba_id_2=None):
        """Comparar dos pruebas"""
        return PruebaFisicaService.comparar_pruebas(int(prueba_id_1), int(prueba_id_2))


class EntrenadorViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Entrenadores.
    """
    
    @swagger_auto_schema(
        operation_description="Listar entrenadores con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('especialidad', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por especialidad"),
            openapi.Parameter('club', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por club asignado"),
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por nombre"),
            openapi.Parameter('usuario_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Buscar por ID de usuario"),
        ],
        responses={200: EntrenadorSerializer(many=True)}
    )
    def list(self, request):
        """Listar entrenadores con filtros opcionales"""
        # Buscar por usuario_id si viene como parámetro
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            return EntrenadorService.obtener_entrenador_por_usuario(int(usuario_id))
        
        criterios = {
            'especialidad': request.query_params.get('especialidad'),
            'club_asignado': request.query_params.get('club'),
            'nombre': request.query_params.get('nombre'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return EntrenadorService.buscar_entrenadores(criterios)
        
        return EntrenadorService.listar_entrenadores()
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo entrenador",
        request_body=EntrenadorSerializer,
        responses={201: EntrenadorSerializer}
    )
    def create(self, request):
        """Crear un nuevo entrenador"""
        return EntrenadorService.crear_entrenador(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener un entrenador por ID",
        responses={200: EntrenadorSerializer, 404: "Entrenador no encontrado"}
    )
    def retrieve(self, request, pk=None):
        """Obtener un entrenador por ID"""
        return EntrenadorService.obtener_entrenador(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar un entrenador",
        request_body=EntrenadorSerializer,
        responses={200: EntrenadorSerializer, 404: "Entrenador no encontrado"}
    )
    def update(self, request, pk=None):
        """Actualizar un entrenador"""
        return EntrenadorService.actualizar_entrenador(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un entrenador",
        request_body=EntrenadorSerializer,
        responses={200: EntrenadorSerializer, 404: "Entrenador no encontrado"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente un entrenador"""
        return EntrenadorService.actualizar_entrenador(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar un entrenador",
        responses={200: "Entrenador eliminado", 404: "Entrenador no encontrado"}
    )
    def destroy(self, request, pk=None):
        """Eliminar un entrenador"""
        return EntrenadorService.eliminar_entrenador(int(pk))
    
    @swagger_auto_schema(
        operation_description="Obtener grupos asignados a un entrenador",
        responses={200: GrupoAtletaSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='grupos')
    def grupos(self, request, pk=None):
        """Obtener grupos de un entrenador"""
        return EntrenadorService.obtener_grupos_entrenador(int(pk))
    
    @swagger_auto_schema(
        operation_description="Asignar un grupo a un entrenador",
        responses={200: "Grupo asignado", 400: "Error al asignar"}
    )
    @action(detail=True, methods=['post'], url_path='asignar-grupo/(?P<grupo_id>[^/.]+)')
    def asignar_grupo(self, request, pk=None, grupo_id=None):
        """Asignar grupo a un entrenador"""
        return EntrenadorService.asignar_grupo(int(pk), int(grupo_id))
    
    @swagger_auto_schema(
        operation_description="Remover un grupo de un entrenador",
        responses={200: "Grupo removido", 400: "Error al remover"}
    )
    @action(detail=True, methods=['post'], url_path='remover-grupo/(?P<grupo_id>[^/.]+)')
    def remover_grupo(self, request, pk=None, grupo_id=None):
        """Remover grupo de un entrenador"""
        return EntrenadorService.remover_grupo(int(pk), int(grupo_id))


class EstudianteVinculacionViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de Estudiantes de Vinculación.
    """
    
    @swagger_auto_schema(
        operation_description="Listar estudiantes con filtros opcionales",
        manual_parameters=[
            openapi.Parameter('carrera', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por carrera"),
            openapi.Parameter('semestre', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Filtrar por semestre"),
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            description="Filtrar por nombre"),
            openapi.Parameter('usuario_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description="Buscar por ID de usuario"),
        ],
        responses={200: EstudianteVinculacionSerializer(many=True)}
    )
    def list(self, request):
        """Listar estudiantes con filtros opcionales"""
        # Buscar por usuario_id si viene como parámetro
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            return EstudianteVinculacionService.obtener_estudiante_por_usuario(int(usuario_id))
        
        criterios = {
            'carrera': request.query_params.get('carrera'),
            'semestre': request.query_params.get('semestre'),
            'nombre': request.query_params.get('nombre'),
        }
        criterios = {k: v for k, v in criterios.items() if v is not None}
        
        if criterios:
            return EstudianteVinculacionService.buscar_estudiantes(criterios)
        
        return EstudianteVinculacionService.listar_estudiantes()
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo estudiante de vinculación",
        request_body=EstudianteVinculacionSerializer,
        responses={201: EstudianteVinculacionSerializer}
    )
    def create(self, request):
        """Crear un nuevo estudiante"""
        return EstudianteVinculacionService.crear_estudiante(request.data)
    
    @swagger_auto_schema(
        operation_description="Obtener un estudiante por ID",
        responses={200: EstudianteVinculacionSerializer, 404: "Estudiante no encontrado"}
    )
    def retrieve(self, request, pk=None):
        """Obtener un estudiante por ID"""
        return EstudianteVinculacionService.obtener_estudiante(int(pk))
    
    @swagger_auto_schema(
        operation_description="Actualizar un estudiante",
        request_body=EstudianteVinculacionSerializer,
        responses={200: EstudianteVinculacionSerializer, 404: "Estudiante no encontrado"}
    )
    def update(self, request, pk=None):
        """Actualizar un estudiante"""
        return EstudianteVinculacionService.actualizar_estudiante(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un estudiante",
        request_body=EstudianteVinculacionSerializer,
        responses={200: EstudianteVinculacionSerializer, 404: "Estudiante no encontrado"}
    )
    def partial_update(self, request, pk=None):
        """Actualizar parcialmente un estudiante"""
        return EstudianteVinculacionService.actualizar_estudiante(int(pk), request.data)
    
    @swagger_auto_schema(
        operation_description="Eliminar un estudiante",
        responses={200: "Estudiante eliminado", 404: "Estudiante no encontrado"}
    )
    def destroy(self, request, pk=None):
        """Eliminar un estudiante"""
        return EstudianteVinculacionService.eliminar_estudiante(int(pk))
