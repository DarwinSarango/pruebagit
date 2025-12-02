"""
Controladores para Pruebas Antropométricas - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any

from basketball.models import PruebaAntropometrica, Atleta
from basketball.dao import PruebaAntropometricaDAO, AtletaDAO


class PruebaAntropometricaController:
    """Controlador para gestionar operaciones de Pruebas Antropométricas"""
    
    def __init__(self):
        self.dao = PruebaAntropometricaDAO()
        self.atleta_dao = AtletaDAO()
    
    def crear_prueba(self, data: dict) -> PruebaAntropometrica:
        """Crear una nueva prueba antropométrica"""
        # Procesar atleta
        if 'atleta_id' in data:
            atleta_id = data.pop('atleta_id')
            data['atleta'] = self.atleta_dao.find_by_id(atleta_id)
        
        return self.dao.create_from_dict(data)
    
    def obtener_prueba(self, prueba_id: int) -> Optional[PruebaAntropometrica]:
        """Obtener una prueba por ID"""
        return self.dao.find_by_id(prueba_id)
    
    def listar_pruebas(self, activas_solo: bool = True) -> List[PruebaAntropometrica]:
        """Listar todas las pruebas"""
        return self.dao.find_all_as_list(active_only=activas_solo)
    
    def actualizar_prueba(self, prueba_id: int, data: dict) -> Optional[PruebaAntropometrica]:
        """Actualizar una prueba existente"""
        # No permitir cambiar atleta_id
        data.pop('atleta_id', None)
        return self.dao.update_from_dict(prueba_id, data)
    
    def eliminar_prueba(self, prueba_id: int, soft_delete: bool = True) -> bool:
        """Eliminar una prueba (soft delete por defecto)"""
        return self.dao.delete(prueba_id, soft=soft_delete)
    
    def obtener_pruebas_atleta(self, atleta_id: int) -> List[PruebaAntropometrica]:
        """Obtener todas las pruebas de un atleta"""
        return self.dao.find_by_atleta(atleta_id)
    
    def obtener_ultima_prueba_atleta(self, atleta_id: int) -> Optional[PruebaAntropometrica]:
        """Obtener la última prueba de un atleta"""
        return self.dao.find_ultima_by_atleta(atleta_id)
    
    def comparar_pruebas(self, prueba_id_1: int, prueba_id_2: int) -> dict:
        """Comparar dos pruebas antropométricas"""
        prueba1 = self.dao.find_by_id(prueba_id_1)
        prueba2 = self.dao.find_by_id(prueba_id_2)
        
        if not prueba1 or not prueba2:
            return {"error": "Una o ambas pruebas no existen"}
        
        return {
            "prueba_1": {
                "id": prueba1.id,
                "fecha": prueba1.fecha_registro,
                "imc": prueba1.indice_masa_corporal,
                "estatura": prueba1.estatura,
                "peso": prueba1.peso
            },
            "prueba_2": {
                "id": prueba2.id,
                "fecha": prueba2.fecha_registro,
                "imc": prueba2.indice_masa_corporal,
                "estatura": prueba2.estatura,
                "peso": prueba2.peso
            },
            "diferencias": {
                "imc": round((prueba1.indice_masa_corporal or 0) - (prueba2.indice_masa_corporal or 0), 2),
                "estatura": round(prueba1.estatura - prueba2.estatura, 2),
                "peso": round(prueba1.peso - prueba2.peso, 2)
            }
        }
    
    def buscar_pruebas(self, criterios: dict) -> List[PruebaAntropometrica]:
        """Buscar pruebas por criterios"""
        filters = {}
        
        if criterios.get('atleta_id'):
            filters['atleta_id'] = criterios['atleta_id']
        if criterios.get('fecha_desde'):
            filters['fecha_registro__gte'] = criterios['fecha_desde']
        if criterios.get('fecha_hasta'):
            filters['fecha_registro__lte'] = criterios['fecha_hasta']
        if criterios.get('imc_min'):
            filters['indice_masa_corporal__gte'] = criterios['imc_min']
        if criterios.get('imc_max'):
            filters['indice_masa_corporal__lte'] = criterios['imc_max']
        
        return list(self.dao.find_by_criteria(filters, active_only=True))
    
    def obtener_estadisticas_atleta(self, atleta_id: int) -> Dict[str, Any]:
        """Obtener estadísticas de un atleta"""
        return self.dao.get_estadisticas_by_atleta(atleta_id)
    
    def obtener_promedio_imc_grupo(self, grupo_id: int) -> Optional[float]:
        """Obtener promedio de IMC de un grupo"""
        return self.dao.get_promedio_imc_by_grupo(grupo_id)


# Instancia singleton para compatibilidad
_controller = PruebaAntropometricaController()

# Métodos estáticos para compatibilidad hacia atrás
crear_prueba = lambda data: _controller.crear_prueba(data)
obtener_prueba = lambda id: _controller.obtener_prueba(id)
listar_pruebas = lambda activas=True: _controller.listar_pruebas(activas)
actualizar_prueba = lambda id, data: _controller.actualizar_prueba(id, data)
eliminar_prueba = lambda id, soft=True: _controller.eliminar_prueba(id, soft)
obtener_pruebas_atleta = lambda id: _controller.obtener_pruebas_atleta(id)
obtener_ultima_prueba_atleta = lambda id: _controller.obtener_ultima_prueba_atleta(id)
comparar_pruebas = lambda id1, id2: _controller.comparar_pruebas(id1, id2)
buscar_pruebas = lambda c: _controller.buscar_pruebas(c)
