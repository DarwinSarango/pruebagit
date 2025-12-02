"""
Controladores para GrupoAtleta - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any

from basketball.models import GrupoAtleta, Atleta
from basketball.dao import GrupoAtletaDAO, AtletaDAO


class GrupoAtletaController:
    """Controlador para gestionar operaciones de GrupoAtleta"""
    
    def __init__(self):
        self.dao = GrupoAtletaDAO()
        self.atleta_dao = AtletaDAO()
    
    def crear_grupo(self, data: dict) -> GrupoAtleta:
        """Crear un nuevo grupo de atletas"""
        return self.dao.create_from_dict(data)
    
    def obtener_grupo(self, grupo_id: int) -> Optional[GrupoAtleta]:
        """Obtener un grupo por ID"""
        return self.dao.find_by_id(grupo_id)
    
    def listar_grupos(self, activos_solo: bool = True) -> List[GrupoAtleta]:
        """Listar todos los grupos"""
        return self.dao.find_all_as_list(active_only=activos_solo)
    
    def actualizar_grupo(self, grupo_id: int, data: dict) -> Optional[GrupoAtleta]:
        """Actualizar un grupo existente"""
        return self.dao.update_from_dict(grupo_id, data)
    
    def eliminar_grupo(self, grupo_id: int, soft_delete: bool = True) -> bool:
        """Eliminar un grupo (soft delete por defecto)"""
        return self.dao.delete(grupo_id, soft=soft_delete)
    
    def obtener_atletas_grupo(self, grupo_id: int) -> List[Atleta]:
        """Obtener todos los atletas de un grupo"""
        return self.atleta_dao.find_by_grupo(grupo_id)
    
    def agregar_atleta_grupo(self, grupo_id: int, atleta_id: int) -> bool:
        """Agregar un atleta a un grupo"""
        grupo = self.dao.find_by_id(grupo_id)
        atleta = self.atleta_dao.find_by_id(atleta_id)
        
        if grupo and atleta:
            # Verificar edad del atleta
            if grupo.rango_edad_minima <= atleta.edad <= grupo.rango_edad_maxima:
                self.atleta_dao.update(atleta_id, grupo=grupo)
                return True
        return False
    
    def remover_atleta_grupo(self, atleta_id: int) -> bool:
        """Remover un atleta de su grupo"""
        result = self.atleta_dao.update(atleta_id, grupo=None)
        return result is not None
    
    def buscar_grupos_por_categoria(self, categoria: str) -> List[GrupoAtleta]:
        """Buscar grupos por categoría"""
        return self.dao.find_by_categoria(categoria)
    
    def buscar_grupos_por_edad(self, edad: int) -> List[GrupoAtleta]:
        """Buscar grupos que acepten una edad"""
        return self.dao.find_by_edad(edad)
    
    def obtener_grupos_con_conteo(self) -> List[Dict[str, Any]]:
        """Obtener grupos con conteo de atletas"""
        return self.dao.get_grupos_con_atletas()
    
    def paginar_grupos(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Obtener grupos paginados"""
        return self.dao.paginate(page, page_size, active_only=True)


# Instancia singleton para compatibilidad
_controller = GrupoAtletaController()

# Métodos estáticos para compatibilidad hacia atrás
crear_grupo = lambda data: _controller.crear_grupo(data)
obtener_grupo = lambda id: _controller.obtener_grupo(id)
listar_grupos = lambda activos=True: _controller.listar_grupos(activos)
actualizar_grupo = lambda id, data: _controller.actualizar_grupo(id, data)
eliminar_grupo = lambda id, soft=True: _controller.eliminar_grupo(id, soft)
obtener_atletas_grupo = lambda id: _controller.obtener_atletas_grupo(id)
agregar_atleta_grupo = lambda g_id, a_id: _controller.agregar_atleta_grupo(g_id, a_id)
remover_atleta_grupo = lambda id: _controller.remover_atleta_grupo(id)
buscar_grupos_por_categoria = lambda cat: _controller.buscar_grupos_por_categoria(cat)
