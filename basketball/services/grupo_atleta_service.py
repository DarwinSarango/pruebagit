"""
Servicio API para Grupos de Atletas - Usando DAO
"""

from basketball.controllers.grupo_atleta_controller import GrupoAtletaController
from basketball.services.api_response import APIResponse
from basketball.serializers import GrupoAtletaSerializer, AtletaSerializer


class GrupoAtletaService:
    """Servicio para operaciones de GrupoAtleta a través de API"""
    
    _controller = GrupoAtletaController()
    
    @classmethod
    def crear_grupo(cls, data: dict):
        """Crear un nuevo grupo de atletas"""
        try:
            grupo = cls._controller.crear_grupo(data)
            serializer = GrupoAtletaSerializer(grupo)
            return APIResponse.created(
                data=serializer.data,
                message="Grupo de atletas creado exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear grupo de atletas",
                errors=str(e)
            )
    
    @classmethod
    def obtener_grupo(cls, grupo_id: int):
        """Obtener un grupo por ID"""
        grupo = cls._controller.obtener_grupo(grupo_id)
        if grupo:
            serializer = GrupoAtletaSerializer(grupo)
            return APIResponse.success(
                data=serializer.data,
                message="Grupo encontrado"
            )
        return APIResponse.not_found(
            message="Grupo no encontrado",
            resource=f"Grupo con ID {grupo_id}"
        )
    
    @classmethod
    def listar_grupos(cls, activos_solo: bool = True):
        """Listar todos los grupos"""
        grupos = cls._controller.listar_grupos(activos_solo)
        serializer = GrupoAtletaSerializer(grupos, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(grupos)} grupos"
        )
    
    @classmethod
    def actualizar_grupo(cls, grupo_id: int, data: dict):
        """Actualizar un grupo"""
        grupo = cls._controller.actualizar_grupo(grupo_id, data)
        if grupo:
            serializer = GrupoAtletaSerializer(grupo)
            return APIResponse.success(
                data=serializer.data,
                message="Grupo actualizado exitosamente"
            )
        return APIResponse.not_found(
            message="Grupo no encontrado",
            resource=f"Grupo con ID {grupo_id}"
        )
    
    @classmethod
    def eliminar_grupo(cls, grupo_id: int, soft_delete: bool = True):
        """Eliminar un grupo"""
        if cls._controller.eliminar_grupo(grupo_id, soft_delete):
            return APIResponse.success(
                message="Grupo eliminado exitosamente"
            )
        return APIResponse.not_found(
            message="Grupo no encontrado",
            resource=f"Grupo con ID {grupo_id}"
        )
    
    @classmethod
    def obtener_atletas_grupo(cls, grupo_id: int):
        """Obtener atletas de un grupo"""
        atletas = cls._controller.obtener_atletas_grupo(grupo_id)
        serializer = AtletaSerializer(atletas, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(atletas)} atletas en el grupo"
        )
    
    @classmethod
    def agregar_atleta_grupo(cls, grupo_id: int, atleta_id: int):
        """Agregar un atleta a un grupo"""
        if cls._controller.agregar_atleta_grupo(grupo_id, atleta_id):
            return APIResponse.success(
                message="Atleta agregado al grupo exitosamente"
            )
        return APIResponse.error(
            message="No se pudo agregar el atleta al grupo. Verifique que la edad del atleta esté en el rango del grupo."
        )
    
    @classmethod
    def remover_atleta_grupo(cls, atleta_id: int):
        """Remover un atleta de su grupo"""
        if cls._controller.remover_atleta_grupo(atleta_id):
            return APIResponse.success(
                message="Atleta removido del grupo exitosamente"
            )
        return APIResponse.not_found(
            message="Atleta no encontrado"
        )
    
    @classmethod
    def buscar_grupos_por_categoria(cls, categoria: str):
        """Buscar grupos por categoría"""
        grupos = cls._controller.buscar_grupos_por_categoria(categoria)
        serializer = GrupoAtletaSerializer(grupos, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(grupos)} grupos"
        )
