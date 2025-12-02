"""
Servicio API para Entrenadores - Usando DAO
"""

from basketball.controllers.entrenador_controller import EntrenadorController
from basketball.services.api_response import APIResponse
from basketball.serializers import EntrenadorSerializer, GrupoAtletaSerializer


class EntrenadorService:
    """Servicio para operaciones de Entrenador a través de API"""
    
    _controller = EntrenadorController()
    
    @classmethod
    def crear_entrenador(cls, data: dict):
        """Crear un nuevo entrenador"""
        try:
            entrenador = cls._controller.crear_entrenador(data)
            serializer = EntrenadorSerializer(entrenador)
            return APIResponse.created(
                data=serializer.data,
                message="Entrenador creado exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear entrenador",
                errors=str(e)
            )
    
    @classmethod
    def obtener_entrenador(cls, entrenador_id: int):
        """Obtener un entrenador por ID"""
        entrenador = cls._controller.obtener_entrenador(entrenador_id)
        if entrenador:
            serializer = EntrenadorSerializer(entrenador)
            return APIResponse.success(
                data=serializer.data,
                message="Entrenador encontrado"
            )
        return APIResponse.not_found(
            message="Entrenador no encontrado",
            resource=f"Entrenador con ID {entrenador_id}"
        )
    
    @classmethod
    def obtener_entrenador_por_usuario(cls, usuario_id: int):
        """Obtener un entrenador por ID de usuario"""
        entrenador = cls._controller.obtener_entrenador_por_usuario(usuario_id)
        if entrenador:
            serializer = EntrenadorSerializer(entrenador)
            return APIResponse.success(
                data=serializer.data,
                message="Entrenador encontrado"
            )
        return APIResponse.not_found(
            message="Entrenador no encontrado para este usuario"
        )
    
    @classmethod
    def listar_entrenadores(cls):
        """Listar todos los entrenadores"""
        entrenadores = cls._controller.listar_entrenadores()
        serializer = EntrenadorSerializer(entrenadores, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(entrenadores)} entrenadores"
        )
    
    @classmethod
    def actualizar_entrenador(cls, entrenador_id: int, data: dict):
        """Actualizar un entrenador"""
        entrenador = cls._controller.actualizar_entrenador(entrenador_id, data)
        if entrenador:
            serializer = EntrenadorSerializer(entrenador)
            return APIResponse.success(
                data=serializer.data,
                message="Entrenador actualizado exitosamente"
            )
        return APIResponse.not_found(
            message="Entrenador no encontrado",
            resource=f"Entrenador con ID {entrenador_id}"
        )
    
    @classmethod
    def eliminar_entrenador(cls, entrenador_id: int):
        """Eliminar un entrenador"""
        if cls._controller.eliminar_entrenador(entrenador_id):
            return APIResponse.success(
                message="Entrenador eliminado exitosamente"
            )
        return APIResponse.not_found(
            message="Entrenador no encontrado",
            resource=f"Entrenador con ID {entrenador_id}"
        )
    
    @classmethod
    def asignar_grupo(cls, entrenador_id: int, grupo_id: int):
        """Asignar un grupo a un entrenador"""
        if cls._controller.asignar_grupo(entrenador_id, grupo_id):
            return APIResponse.success(
                message="Grupo asignado al entrenador exitosamente"
            )
        return APIResponse.error(
            message="No se pudo asignar el grupo al entrenador"
        )
    
    @classmethod
    def remover_grupo(cls, entrenador_id: int, grupo_id: int):
        """Remover un grupo de un entrenador"""
        if cls._controller.remover_grupo(entrenador_id, grupo_id):
            return APIResponse.success(
                message="Grupo removido del entrenador exitosamente"
            )
        return APIResponse.error(
            message="No se pudo remover el grupo del entrenador"
        )
    
    @classmethod
    def obtener_grupos_entrenador(cls, entrenador_id: int):
        """Obtener grupos de un entrenador"""
        grupos = cls._controller.obtener_grupos_entrenador(entrenador_id)
        serializer = GrupoAtletaSerializer(grupos, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(grupos)} grupos"
        )
    
    @classmethod
    def buscar_entrenadores(cls, criterios: dict):
        """Buscar entrenadores por criterios"""
        entrenadores = cls._controller.buscar_entrenadores(criterios)
        serializer = EntrenadorSerializer(entrenadores, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(entrenadores)} entrenadores"
        )
