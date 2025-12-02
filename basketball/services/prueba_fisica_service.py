"""
Servicio API para Pruebas Físicas - Usando DAO
"""

from basketball.controllers.prueba_fisica_controller import PruebaFisicaController
from basketball.services.api_response import APIResponse
from basketball.serializers import PruebaFisicaSerializer


class PruebaFisicaService:
    """Servicio para operaciones de Pruebas Físicas a través de API"""
    
    _controller = PruebaFisicaController()
    
    @classmethod
    def crear_prueba(cls, data: dict):
        """Crear una nueva prueba física"""
        try:
            prueba = cls._controller.crear_prueba(data)
            serializer = PruebaFisicaSerializer(prueba)
            return APIResponse.created(
                data=serializer.data,
                message="Prueba física creada exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear prueba física",
                errors=str(e)
            )
    
    @classmethod
    def obtener_prueba(cls, prueba_id: int):
        """Obtener una prueba por ID"""
        prueba = cls._controller.obtener_prueba(prueba_id)
        if prueba:
            serializer = PruebaFisicaSerializer(prueba)
            return APIResponse.success(
                data=serializer.data,
                message="Prueba encontrada"
            )
        return APIResponse.not_found(
            message="Prueba no encontrada",
            resource=f"Prueba con ID {prueba_id}"
        )
    
    @classmethod
    def listar_pruebas(cls, activas_solo: bool = True):
        """Listar todas las pruebas"""
        pruebas = cls._controller.listar_pruebas(activas_solo)
        serializer = PruebaFisicaSerializer(pruebas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(pruebas)} pruebas"
        )
    
    @classmethod
    def actualizar_prueba(cls, prueba_id: int, data: dict):
        """Actualizar una prueba"""
        prueba = cls._controller.actualizar_prueba(prueba_id, data)
        if prueba:
            serializer = PruebaFisicaSerializer(prueba)
            return APIResponse.success(
                data=serializer.data,
                message="Prueba actualizada exitosamente"
            )
        return APIResponse.not_found(
            message="Prueba no encontrada",
            resource=f"Prueba con ID {prueba_id}"
        )
    
    @classmethod
    def eliminar_prueba(cls, prueba_id: int, soft_delete: bool = True):
        """Eliminar una prueba"""
        if cls._controller.eliminar_prueba(prueba_id, soft_delete):
            return APIResponse.success(
                message="Prueba eliminada exitosamente"
            )
        return APIResponse.not_found(
            message="Prueba no encontrada",
            resource=f"Prueba con ID {prueba_id}"
        )
    
    @classmethod
    def obtener_pruebas_atleta(cls, atleta_id: int):
        """Obtener pruebas de un atleta"""
        pruebas = cls._controller.obtener_pruebas_atleta(atleta_id)
        serializer = PruebaFisicaSerializer(pruebas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(pruebas)} pruebas"
        )
    
    @classmethod
    def obtener_pruebas_por_tipo(cls, atleta_id: int, tipo_prueba: str):
        """Obtener pruebas de un atleta por tipo"""
        pruebas = cls._controller.obtener_pruebas_por_tipo(atleta_id, tipo_prueba)
        serializer = PruebaFisicaSerializer(pruebas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(pruebas)} pruebas de tipo {tipo_prueba}"
        )
    
    @classmethod
    def comparar_pruebas(cls, prueba_id_1: int, prueba_id_2: int):
        """Comparar dos pruebas"""
        resultado = cls._controller.comparar_pruebas(prueba_id_1, prueba_id_2)
        if "error" in resultado:
            return APIResponse.error(message=resultado["error"])
        return APIResponse.success(
            data=resultado,
            message="Comparación realizada exitosamente"
        )
    
    @classmethod
    def buscar_pruebas(cls, criterios: dict):
        """Buscar pruebas por criterios"""
        pruebas = cls._controller.buscar_pruebas(criterios)
        serializer = PruebaFisicaSerializer(pruebas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(pruebas)} pruebas"
        )
    
    @classmethod
    def obtener_tipos_prueba(cls):
        """Obtener tipos de prueba disponibles"""
        tipos = cls._controller.obtener_tipos_prueba()
        return APIResponse.success(
            data=tipos,
            message="Tipos de prueba obtenidos"
        )
    
    @classmethod
    def obtener_estadisticas_atleta(cls, atleta_id: int):
        """Obtener estadísticas de un atleta"""
        estadisticas = cls._controller.obtener_estadisticas_atleta(atleta_id)
        return APIResponse.success(
            data=estadisticas,
            message="Estadísticas obtenidas"
        )
