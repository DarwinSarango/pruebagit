"""
Servicio para Atleta
TODO: Implementar la lógica de negocio para Atleta
"""


class AtletaService:
    """Servicio para la lógica de negocio de Atleta"""
    
    def __init__(self):
        # TODO: Inicializar DAO
        pass
    
    def listar_atletas(self, solo_activos: bool = True):
        """Listar todos los atletas"""
        # TODO: Implementar
        pass
    
    def obtener_atleta(self, atleta_id: int):
        """Obtener un atleta por ID"""
        # TODO: Implementar
        pass
    
    def crear_atleta(self, datos: dict):
        """Crear un nuevo atleta"""
        # TODO: Implementar validaciones y lógica de negocio
        pass
    
    def actualizar_atleta(self, atleta_id: int, datos: dict):
        """Actualizar un atleta"""
        # TODO: Implementar validaciones y lógica de negocio
        pass
    
    def eliminar_atleta(self, atleta_id: int):
        """Eliminar un atleta (soft delete)"""
        # TODO: Implementar
        pass
    
    def buscar_por_dni(self, dni: str):
        """Buscar atleta por DNI"""
        # TODO: Implementar
        pass
    
    def asignar_grupo(self, atleta_id: int, grupo_id: int):
        """Asignar un grupo a un atleta"""
        # TODO: Implementar validaciones
        pass
