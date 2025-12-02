"""
Controladores para Pruebas Físicas - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any

from basketball.models import PruebaFisica, Atleta, TipoPrueba
from basketball.dao import PruebaFisicaDAO, AtletaDAO


class PruebaFisicaController:
    """Controlador para gestionar operaciones de Pruebas Físicas"""
    
    def __init__(self):
        self.dao = PruebaFisicaDAO()
        self.atleta_dao = AtletaDAO()
    
    def crear_prueba(self, data: dict) -> PruebaFisica:
        """Crear una nueva prueba física"""
        # Procesar atleta
        if 'atleta_id' in data:
            atleta_id = data.pop('atleta_id')
            data['atleta'] = self.atleta_dao.find_by_id(atleta_id)
        
        return self.dao.create_from_dict(data)
    
    def obtener_prueba(self, prueba_id: int) -> Optional[PruebaFisica]:
        """Obtener una prueba por ID"""
        return self.dao.find_by_id(prueba_id)
    
    def listar_pruebas(self, activas_solo: bool = True) -> List[PruebaFisica]:
        """Listar todas las pruebas"""
        return self.dao.find_all_as_list(active_only=activas_solo)
    
    def actualizar_prueba(self, prueba_id: int, data: dict) -> Optional[PruebaFisica]:
        """Actualizar una prueba existente"""
        # No permitir cambiar atleta_id
        data.pop('atleta_id', None)
        return self.dao.update_from_dict(prueba_id, data)
    
    def eliminar_prueba(self, prueba_id: int, soft_delete: bool = True) -> bool:
        """Eliminar una prueba (soft delete por defecto)"""
        return self.dao.delete(prueba_id, soft=soft_delete)
    
    def obtener_pruebas_atleta(self, atleta_id: int) -> List[PruebaFisica]:
        """Obtener todas las pruebas de un atleta"""
        return self.dao.find_by_atleta(atleta_id)
    
    def obtener_pruebas_por_tipo(self, atleta_id: int, tipo_prueba: str) -> List[PruebaFisica]:
        """Obtener pruebas de un atleta por tipo"""
        return self.dao.find_by_atleta_y_tipo(atleta_id, tipo_prueba)
    
    def obtener_ultima_prueba_por_tipo(self, atleta_id: int, tipo_prueba: str) -> Optional[PruebaFisica]:
        """Obtener la última prueba de un tipo específico"""
        return self.dao.find_ultima_by_atleta_y_tipo(atleta_id, tipo_prueba)
    
    def comparar_pruebas(self, prueba_id_1: int, prueba_id_2: int) -> dict:
        """Comparar dos pruebas físicas"""
        prueba1 = self.dao.find_by_id(prueba_id_1)
        prueba2 = self.dao.find_by_id(prueba_id_2)
        
        if not prueba1 or not prueba2:
            return {"error": "Una o ambas pruebas no existen"}
        
        return prueba1.comparar_resultados(prueba2)
    
    def buscar_pruebas(self, criterios: dict) -> List[PruebaFisica]:
        """Buscar pruebas por criterios"""
        filters = {}
        
        if criterios.get('atleta_id'):
            filters['atleta_id'] = criterios['atleta_id']
        if criterios.get('tipo_prueba'):
            filters['tipo_prueba'] = criterios['tipo_prueba']
        if criterios.get('fecha_desde'):
            filters['fecha_registro__gte'] = criterios['fecha_desde']
        if criterios.get('fecha_hasta'):
            filters['fecha_registro__lte'] = criterios['fecha_hasta']
        if criterios.get('resultado_min'):
            filters['resultado__gte'] = criterios['resultado_min']
        if criterios.get('resultado_max'):
            filters['resultado__lte'] = criterios['resultado_max']
        
        return list(self.dao.find_by_criteria(filters, active_only=True))
    
    def obtener_tipos_prueba(self) -> List[dict]:
        """Obtener los tipos de prueba disponibles"""
        return [{"valor": choice[0], "etiqueta": choice[1]} for choice in TipoPrueba.choices]
    
    def obtener_estadisticas_atleta(self, atleta_id: int) -> dict:
        """Obtener estadísticas de pruebas de un atleta"""
        return self.dao.get_estadisticas_by_atleta(atleta_id)
    
    def obtener_promedio_por_tipo(self, tipo_prueba: str) -> Optional[float]:
        """Obtener promedio de resultados por tipo"""
        return self.dao.get_promedio_by_tipo(tipo_prueba)


# Instancia singleton para compatibilidad
_controller = PruebaFisicaController()

# Métodos estáticos para compatibilidad hacia atrás
crear_prueba = lambda data: _controller.crear_prueba(data)
obtener_prueba = lambda id: _controller.obtener_prueba(id)
listar_pruebas = lambda activas=True: _controller.listar_pruebas(activas)
actualizar_prueba = lambda id, data: _controller.actualizar_prueba(id, data)
eliminar_prueba = lambda id, soft=True: _controller.eliminar_prueba(id, soft)
obtener_pruebas_atleta = lambda id: _controller.obtener_pruebas_atleta(id)
obtener_pruebas_por_tipo = lambda id, tipo: _controller.obtener_pruebas_por_tipo(id, tipo)
obtener_ultima_prueba_por_tipo = lambda id, tipo: _controller.obtener_ultima_prueba_por_tipo(id, tipo)
comparar_pruebas = lambda id1, id2: _controller.comparar_pruebas(id1, id2)
buscar_pruebas = lambda c: _controller.buscar_pruebas(c)
obtener_tipos_prueba = lambda: _controller.obtener_tipos_prueba()
obtener_estadisticas_atleta = lambda id: _controller.obtener_estadisticas_atleta(id)
