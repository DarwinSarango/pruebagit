"""
Controladores para Inscripción - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any
from datetime import date

from basketball.models import Inscripcion, Atleta, TipoInscripcion
from basketball.dao import InscripcionDAO, AtletaDAO


class InscripcionController:
    """Controlador para gestionar operaciones de Inscripción"""
    
    def __init__(self):
        self.dao = InscripcionDAO()
        self.atleta_dao = AtletaDAO()
    
    def crear_inscripcion(self, data: dict) -> Inscripcion:
        """Crear una nueva inscripción"""
        # Procesar atleta
        if 'atleta_id' in data:
            atleta_id = data.pop('atleta_id')
            data['atleta'] = self.atleta_dao.find_by_id(atleta_id)
        
        # Valores por defecto
        if 'fecha_inscripcion' not in data:
            data['fecha_inscripcion'] = date.today()
        if 'tipo_inscripcion' not in data:
            data['tipo_inscripcion'] = TipoInscripcion.NUEVO
        if 'habilitada' not in data:
            data['habilitada'] = False
        
        return self.dao.create_from_dict(data)
    
    def obtener_inscripcion(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Obtener una inscripción por ID"""
        return self.dao.find_by_id(inscripcion_id)
    
    def listar_inscripciones(self) -> List[Inscripcion]:
        """Listar todas las inscripciones"""
        return self.dao.find_all_as_list()
    
    def listar_inscripciones_habilitadas(self) -> List[Inscripcion]:
        """Listar inscripciones habilitadas"""
        return self.dao.find_habilitadas()
    
    def listar_inscripciones_pendientes(self) -> List[Inscripcion]:
        """Listar inscripciones pendientes de habilitación"""
        return self.dao.find_pendientes()
    
    def actualizar_inscripcion(self, inscripcion_id: int, data: dict) -> Optional[Inscripcion]:
        """Actualizar una inscripción existente"""
        return self.dao.update_from_dict(inscripcion_id, data)
    
    def habilitar_inscripcion(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Habilitar una inscripción"""
        return self.dao.habilitar(inscripcion_id)
    
    def deshabilitar_inscripcion(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Deshabilitar una inscripción"""
        return self.dao.deshabilitar(inscripcion_id)
    
    def eliminar_inscripcion(self, inscripcion_id: int) -> bool:
        """Eliminar una inscripción"""
        return self.dao.hard_delete(inscripcion_id)
    
    def obtener_inscripciones_atleta(self, atleta_id: int) -> List[Inscripcion]:
        """Obtener todas las inscripciones de un atleta"""
        return self.dao.find_by_atleta(atleta_id)
    
    def buscar_inscripciones(self, criterios: dict) -> List[Inscripcion]:
        """Buscar inscripciones por criterios"""
        filters = {}
        
        if criterios.get('tipo_inscripcion'):
            filters['tipo_inscripcion'] = criterios['tipo_inscripcion']
        if criterios.get('habilitada') is not None:
            filters['habilitada'] = criterios['habilitada']
        if criterios.get('fecha_desde'):
            filters['fecha_inscripcion__gte'] = criterios['fecha_desde']
        if criterios.get('fecha_hasta'):
            filters['fecha_inscripcion__lte'] = criterios['fecha_hasta']
        if criterios.get('atleta_id'):
            filters['atleta_id'] = criterios['atleta_id']
        
        return list(self.dao.find_by_criteria(filters))
    
    def tiene_inscripcion_activa(self, atleta_id: int) -> bool:
        """Verificar si un atleta tiene inscripción activa"""
        return self.dao.tiene_inscripcion_activa(atleta_id)
    
    def paginar_inscripciones(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Obtener inscripciones paginadas"""
        return self.dao.paginate(page, page_size)


# Instancia singleton para compatibilidad
_controller = InscripcionController()

# Métodos estáticos para compatibilidad hacia atrás
crear_inscripcion = lambda data: _controller.crear_inscripcion(data)
obtener_inscripcion = lambda id: _controller.obtener_inscripcion(id)
listar_inscripciones = lambda: _controller.listar_inscripciones()
listar_inscripciones_habilitadas = lambda: _controller.listar_inscripciones_habilitadas()
listar_inscripciones_pendientes = lambda: _controller.listar_inscripciones_pendientes()
actualizar_inscripcion = lambda id, data: _controller.actualizar_inscripcion(id, data)
habilitar_inscripcion = lambda id: _controller.habilitar_inscripcion(id)
deshabilitar_inscripcion = lambda id: _controller.deshabilitar_inscripcion(id)
eliminar_inscripcion = lambda id: _controller.eliminar_inscripcion(id)
obtener_inscripciones_atleta = lambda id: _controller.obtener_inscripciones_atleta(id)
buscar_inscripciones = lambda c: _controller.buscar_inscripciones(c)
