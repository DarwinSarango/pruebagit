"""
Servicio para GrupoAtleta
TODO: Implementar la lógica de negocio para GrupoAtleta
"""


class GrupoAtletaService:
    """Servicio para la lógica de negocio de GrupoAtleta"""
    
    def __init__(self):
        # TODO: Inicializar DAO
        pass
    
    def listar_grupos(self, solo_activos: bool = True):
        """Listar todos los grupos"""
        # TODO: Implementar
        pass
    
    def obtener_grupo(self, grupo_id: int):
        """Obtener un grupo por ID"""
        # TODO: Implementar
        pass
    
    def crear_grupo(self, datos: dict):
        """Crear un nuevo grupo"""
        # TODO: Implementar validaciones y lógica de negocio
        pass
    
    def actualizar_grupo(self, grupo_id: int, datos: dict):
        """Actualizar un grupo"""
        # TODO: Implementar validaciones y lógica de negocio
        pass
    
    def eliminar_grupo(self, grupo_id: int):
        """Eliminar un grupo (soft delete)"""
        # TODO: Implementar
        pass
    
    def agregar_atleta(self, grupo_id: int, atleta_id: int):
        """Agregar un atleta al grupo"""
        # TODO: Implementar validaciones (rango de edad, etc.)
        pass
    
    def remover_atleta(self, grupo_id: int, atleta_id: int):
        """Remover un atleta del grupo"""
        # TODO: Implementar
        pass
    
    def listar_atletas_del_grupo(self, grupo_id: int):
        """Listar atletas de un grupo"""
        # TODO: Implementar
        pass
