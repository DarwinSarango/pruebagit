"""
Servicio API para Atletas - Usando DAO
"""

from basketball.controllers.atleta_controller import AtletaController
from basketball.services.api_response import APIResponse
from basketball.serializers import AtletaSerializer


class AtletaService:
    """Servicio para operaciones de Atleta a través de API"""
    
    _controller = AtletaController()
    
    @classmethod
    def crear_atleta(cls, data: dict):
        """Crear un nuevo atleta"""
        try:
            atleta = cls._controller.crear_atleta(data)
            serializer = AtletaSerializer(atleta)
            return APIResponse.created(
                data=serializer.data,
                message="Atleta creado exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear atleta",
                errors=str(e)
            )
    
    @classmethod
    def obtener_atleta(cls, atleta_id: int):
        """Obtener un atleta por ID"""
        atleta = cls._controller.obtener_atleta(atleta_id)
        if atleta:
            serializer = AtletaSerializer(atleta)
            return APIResponse.success(
                data=serializer.data,
                message="Atleta encontrado"
            )
        return APIResponse.not_found(
            message="Atleta no encontrado",
            resource=f"Atleta con ID {atleta_id}"
        )
    
    @classmethod
    def obtener_atleta_por_dni(cls, dni: str):
        """Obtener un atleta por DNI"""
        atleta = cls._controller.obtener_atleta_por_dni(dni)
        if atleta:
            serializer = AtletaSerializer(atleta)
            return APIResponse.success(
                data=serializer.data,
                message="Atleta encontrado"
            )
        return APIResponse.not_found(
            message="Atleta no encontrado",
            resource=f"Atleta con DNI {dni}"
        )
    
    @classmethod
    def listar_atletas(cls, activos_solo: bool = True):
        """Listar todos los atletas"""
        atletas = cls._controller.listar_atletas(activos_solo)
        serializer = AtletaSerializer(atletas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(atletas)} atletas"
        )
    
    @classmethod
    def actualizar_atleta(cls, atleta_id: int, data: dict):
        """Actualizar un atleta"""
        atleta = cls._controller.actualizar_atleta(atleta_id, data)
        if atleta:
            serializer = AtletaSerializer(atleta)
            return APIResponse.success(
                data=serializer.data,
                message="Atleta actualizado exitosamente"
            )
        return APIResponse.not_found(
            message="Atleta no encontrado",
            resource=f"Atleta con ID {atleta_id}"
        )
    
    @classmethod
    def eliminar_atleta(cls, atleta_id: int, soft_delete: bool = True):
        """Eliminar un atleta"""
        if cls._controller.eliminar_atleta(atleta_id, soft_delete):
            return APIResponse.success(
                message="Atleta eliminado exitosamente"
            )
        return APIResponse.not_found(
            message="Atleta no encontrado",
            resource=f"Atleta con ID {atleta_id}"
        )
    
    @classmethod
    def buscar_atletas(cls, criterios: dict):
        """Buscar atletas por criterios"""
        atletas = cls._controller.buscar_atletas(criterios)
        serializer = AtletaSerializer(atletas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(atletas)} atletas"
        )
    
    @classmethod
    def asignar_grupo(cls, atleta_id: int, grupo_id: int):
        """Asignar un atleta a un grupo"""
        atleta = cls._controller.asignar_grupo(atleta_id, grupo_id)
        if atleta:
            serializer = AtletaSerializer(atleta)
            return APIResponse.success(
                data=serializer.data,
                message="Atleta asignado al grupo exitosamente"
            )
        return APIResponse.not_found(
            message="Atleta o grupo no encontrado"
        )
