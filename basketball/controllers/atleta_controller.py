"""
Controladores para Atleta - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime

from basketball.models import Atleta, GrupoAtleta
from basketball.dao import AtletaDAO, GrupoAtletaDAO


class AtletaController:
    """Controlador para gestionar operaciones de Atleta"""
    
    def __init__(self):
        self.dao = AtletaDAO()
        self.grupo_dao = GrupoAtletaDAO()
    
    def _parse_date(self, date_value):
        """Convertir fecha de string a date si es necesario"""
        if date_value is None:
            return None
        if isinstance(date_value, date):
            return date_value
        if isinstance(date_value, datetime):
            return date_value.date()
        if isinstance(date_value, str):
            return datetime.strptime(date_value, '%Y-%m-%d').date()
        return date_value
    
    def crear_atleta(self, data: dict) -> Atleta:
        """Crear un nuevo atleta"""
        data = data.copy()  # No modificar el original
        
        # Convertir fecha_nacimiento si viene como string
        if 'fecha_nacimiento' in data:
            data['fecha_nacimiento'] = self._parse_date(data['fecha_nacimiento'])
        
        # Procesar grupo si viene como grupo_id
        if 'grupo_id' in data:
            grupo_id = data.pop('grupo_id')
            if grupo_id:
                data['grupo'] = self.grupo_dao.find_by_id(grupo_id)
        
        return self.dao.create_from_dict(data)
    
    def obtener_atleta(self, atleta_id: int) -> Optional[Atleta]:
        """Obtener un atleta por ID"""
        return self.dao.find_by_id(atleta_id)
    
    def obtener_atleta_por_dni(self, dni: str) -> Optional[Atleta]:
        """Obtener un atleta por DNI"""
        return self.dao.find_by_dni(dni)
    
    def listar_atletas(self, activos_solo: bool = True) -> List[Atleta]:
        """Listar todos los atletas"""
        return self.dao.find_all_as_list(active_only=activos_solo)
    
    def actualizar_atleta(self, atleta_id: int, data: dict) -> Optional[Atleta]:
        """Actualizar un atleta existente"""
        data = data.copy()  # No modificar el original
        
        # Convertir fecha_nacimiento si viene como string
        if 'fecha_nacimiento' in data:
            data['fecha_nacimiento'] = self._parse_date(data['fecha_nacimiento'])
        
        # Procesar grupo si viene como grupo_id
        if 'grupo_id' in data:
            grupo_id = data.pop('grupo_id')
            if grupo_id:
                data['grupo'] = self.grupo_dao.find_by_id(grupo_id)
        
        return self.dao.update_from_dict(atleta_id, data)
    
    def eliminar_atleta(self, atleta_id: int, soft_delete: bool = True) -> bool:
        """Eliminar un atleta (soft delete por defecto)"""
        return self.dao.delete(atleta_id, soft=soft_delete)
    
    def buscar_atletas(self, criterios: dict) -> List[Atleta]:
        """Buscar atletas por criterios"""
        return self.dao.search(criterios)
    
    def asignar_grupo(self, atleta_id: int, grupo_id: int) -> Optional[Atleta]:
        """Asignar un atleta a un grupo"""
        grupo = self.grupo_dao.find_by_id(grupo_id)
        if grupo:
            return self.dao.update(atleta_id, grupo=grupo)
        return None
    
    def obtener_atletas_por_grupo(self, grupo_id: int) -> List[Atleta]:
        """Obtener atletas de un grupo específico"""
        return self.dao.find_by_grupo(grupo_id)
    
    def obtener_atletas_sin_grupo(self) -> List[Atleta]:
        """Obtener atletas sin grupo asignado"""
        return self.dao.find_sin_grupo()
    
    def obtener_atletas_por_rango_edad(self, edad_min: int, edad_max: int) -> List[Atleta]:
        """Obtener atletas por rango de edad"""
        return self.dao.find_by_rango_edad(edad_min, edad_max)
    
    def paginar_atletas(
        self, page: int = 1, page_size: int = 10, activos_solo: bool = True
    ) -> Dict[str, Any]:
        """Obtener atletas paginados"""
        return self.dao.paginate(page, page_size, active_only=activos_solo)
    
    def contar_atletas(self, activos_solo: bool = True) -> int:
        """Contar total de atletas"""
        return self.dao.count(active_only=activos_solo)
    
    def existe_dni(self, dni: str) -> bool:
        """Verificar si ya existe un atleta con el DNI"""
        return self.dao.exists_by_field('dni', dni)
    
    def restaurar_atleta(self, atleta_id: int) -> Optional[Atleta]:
        """Restaurar un atleta eliminado"""
        return self.dao.restore(atleta_id)


# Instancia singleton para uso directo (compatibilidad con código existente)
_controller = AtletaController()

# Métodos estáticos para compatibilidad hacia atrás
crear_atleta = lambda data: _controller.crear_atleta(data)
obtener_atleta = lambda id: _controller.obtener_atleta(id)
obtener_atleta_por_dni = lambda dni: _controller.obtener_atleta_por_dni(dni)
listar_atletas = lambda activos=True: _controller.listar_atletas(activos)
actualizar_atleta = lambda id, data: _controller.actualizar_atleta(id, data)
eliminar_atleta = lambda id, soft=True: _controller.eliminar_atleta(id, soft)
buscar_atletas = lambda criterios: _controller.buscar_atletas(criterios)
asignar_grupo = lambda atleta_id, grupo_id: _controller.asignar_grupo(atleta_id, grupo_id)
