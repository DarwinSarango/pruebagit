"""
Servicio API para Inscripciones - Usando DAO
"""

from basketball.controllers.inscripcion_controller import InscripcionController
from basketball.services.api_response import APIResponse
from basketball.serializers import InscripcionSerializer


class InscripcionService:
    """Servicio para operaciones de Inscripción a través de API"""
    
    _controller = InscripcionController()
    
    @classmethod
    def crear_inscripcion(cls, data: dict):
        """Crear una nueva inscripción"""
        try:
            inscripcion = cls._controller.crear_inscripcion(data)
            serializer = InscripcionSerializer(inscripcion)
            return APIResponse.created(
                data=serializer.data,
                message="Inscripción creada exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear inscripción",
                errors=str(e)
            )
    
    @classmethod
    def obtener_inscripcion(cls, inscripcion_id: int):
        """Obtener una inscripción por ID"""
        inscripcion = cls._controller.obtener_inscripcion(inscripcion_id)
        if inscripcion:
            serializer = InscripcionSerializer(inscripcion)
            return APIResponse.success(
                data=serializer.data,
                message="Inscripción encontrada"
            )
        return APIResponse.not_found(
            message="Inscripción no encontrada",
            resource=f"Inscripción con ID {inscripcion_id}"
        )
    
    @classmethod
    def listar_inscripciones(cls):
        """Listar todas las inscripciones"""
        inscripciones = cls._controller.listar_inscripciones()
        serializer = InscripcionSerializer(inscripciones, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(inscripciones)} inscripciones"
        )
    
    @classmethod
    def listar_inscripciones_habilitadas(cls):
        """Listar inscripciones habilitadas"""
        inscripciones = cls._controller.listar_inscripciones_habilitadas()
        serializer = InscripcionSerializer(inscripciones, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(inscripciones)} inscripciones habilitadas"
        )
    
    @classmethod
    def listar_inscripciones_pendientes(cls):
        """Listar inscripciones pendientes"""
        inscripciones = cls._controller.listar_inscripciones_pendientes()
        serializer = InscripcionSerializer(inscripciones, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(inscripciones)} inscripciones pendientes"
        )
    
    @classmethod
    def actualizar_inscripcion(cls, inscripcion_id: int, data: dict):
        """Actualizar una inscripción"""
        inscripcion = cls._controller.actualizar_inscripcion(inscripcion_id, data)
        if inscripcion:
            serializer = InscripcionSerializer(inscripcion)
            return APIResponse.success(
                data=serializer.data,
                message="Inscripción actualizada exitosamente"
            )
        return APIResponse.not_found(
            message="Inscripción no encontrada",
            resource=f"Inscripción con ID {inscripcion_id}"
        )
    
    @classmethod
    def habilitar_inscripcion(cls, inscripcion_id: int):
        """Habilitar una inscripción"""
        inscripcion = cls._controller.habilitar_inscripcion(inscripcion_id)
        if inscripcion:
            serializer = InscripcionSerializer(inscripcion)
            return APIResponse.success(
                data=serializer.data,
                message="Inscripción habilitada exitosamente"
            )
        return APIResponse.not_found(
            message="Inscripción no encontrada",
            resource=f"Inscripción con ID {inscripcion_id}"
        )
    
    @classmethod
    def deshabilitar_inscripcion(cls, inscripcion_id: int):
        """Deshabilitar una inscripción"""
        inscripcion = cls._controller.deshabilitar_inscripcion(inscripcion_id)
        if inscripcion:
            serializer = InscripcionSerializer(inscripcion)
            return APIResponse.success(
                data=serializer.data,
                message="Inscripción deshabilitada exitosamente"
            )
        return APIResponse.not_found(
            message="Inscripción no encontrada",
            resource=f"Inscripción con ID {inscripcion_id}"
        )
    
    @classmethod
    def eliminar_inscripcion(cls, inscripcion_id: int):
        """Eliminar una inscripción"""
        if cls._controller.eliminar_inscripcion(inscripcion_id):
            return APIResponse.success(
                message="Inscripción eliminada exitosamente"
            )
        return APIResponse.not_found(
            message="Inscripción no encontrada",
            resource=f"Inscripción con ID {inscripcion_id}"
        )
    
    @classmethod
    def obtener_inscripciones_atleta(cls, atleta_id: int):
        """Obtener inscripciones de un atleta"""
        inscripciones = cls._controller.obtener_inscripciones_atleta(atleta_id)
        serializer = InscripcionSerializer(inscripciones, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(inscripciones)} inscripciones"
        )
    
    @classmethod
    def buscar_inscripciones(cls, criterios: dict):
        """Buscar inscripciones por criterios"""
        inscripciones = cls._controller.buscar_inscripciones(criterios)
        serializer = InscripcionSerializer(inscripciones, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(inscripciones)} inscripciones"
        )
