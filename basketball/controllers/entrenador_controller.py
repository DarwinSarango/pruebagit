"""
Controladores para Entrenador - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any

from basketball.models import Entrenador, Usuario, GrupoAtleta
from basketball.dao import EntrenadorDAO, UsuarioDAO, GrupoAtletaDAO


class EntrenadorController:
    """Controlador para gestionar operaciones de Entrenador"""
    
    def __init__(self):
        self.dao = EntrenadorDAO()
        self.usuario_dao = UsuarioDAO()
        self.grupo_dao = GrupoAtletaDAO()
    
    def crear_entrenador(self, data: dict) -> Entrenador:
        """Crear un nuevo entrenador"""
        # Procesar usuario
        if 'usuario_id' in data:
            usuario_id = data.pop('usuario_id')
            data['usuario'] = self.usuario_dao.find_by_id(usuario_id)
        
        # Extraer grupos_ids antes de crear
        grupos_ids = data.pop('grupos_ids', None)
        
        entrenador = self.dao.create_from_dict(data)
        
        # Asignar grupos si se proporcionan
        if grupos_ids:
            for grupo_id in grupos_ids:
                grupo = self.grupo_dao.find_by_id(grupo_id)
                if grupo:
                    entrenador.grupos.add(grupo)
        
        return entrenador
    
    def obtener_entrenador(self, entrenador_id: int) -> Optional[Entrenador]:
        """Obtener un entrenador por ID"""
        return self.dao.find_by_id(entrenador_id)
    
    def obtener_entrenador_por_usuario(self, usuario_id: int) -> Optional[Entrenador]:
        """Obtener un entrenador por ID de usuario"""
        return self.dao.find_by_usuario(usuario_id)
    
    def listar_entrenadores(self) -> List[Entrenador]:
        """Listar todos los entrenadores"""
        return list(self.dao.find_all().filter(usuario__estado=True))
    
    def actualizar_entrenador(self, entrenador_id: int, data: dict) -> Optional[Entrenador]:
        """Actualizar un entrenador existente"""
        entrenador = self.dao.find_by_id(entrenador_id)
        if not entrenador:
            return None
        
        # Manejar grupos separadamente
        grupos_ids = data.pop('grupos_ids', None)
        
        # Actualizar campos básicos
        if data:
            entrenador = self.dao.update_from_dict(entrenador_id, data)
        
        # Actualizar grupos si se proporcionan
        if grupos_ids is not None:
            entrenador.grupos.clear()
            for grupo_id in grupos_ids:
                grupo = self.grupo_dao.find_by_id(grupo_id)
                if grupo:
                    entrenador.grupos.add(grupo)
        
        return entrenador
    
    def eliminar_entrenador(self, entrenador_id: int) -> bool:
        """Eliminar un entrenador"""
        return self.dao.hard_delete(entrenador_id)
    
    def asignar_grupo(self, entrenador_id: int, grupo_id: int) -> bool:
        """Asignar un grupo a un entrenador"""
        result = self.dao.asignar_grupo(entrenador_id, grupo_id)
        return result is not None
    
    def remover_grupo(self, entrenador_id: int, grupo_id: int) -> bool:
        """Remover un grupo de un entrenador"""
        result = self.dao.remover_grupo(entrenador_id, grupo_id)
        return result is not None
    
    def obtener_grupos_entrenador(self, entrenador_id: int) -> List[GrupoAtleta]:
        """Obtener todos los grupos asignados a un entrenador"""
        return self.dao.get_grupos(entrenador_id)
    
    def buscar_entrenadores(self, criterios: dict) -> List[Entrenador]:
        """Buscar entrenadores por criterios"""
        queryset = self.dao.find_all().filter(usuario__estado=True)
        
        if criterios.get('especialidad'):
            queryset = queryset.filter(especialidad__icontains=criterios['especialidad'])
        if criterios.get('club_asignado'):
            queryset = queryset.filter(club_asignado__icontains=criterios['club_asignado'])
        if criterios.get('nombre'):
            queryset = queryset.filter(usuario__nombre__icontains=criterios['nombre'])
        
        return list(queryset)
    
    def buscar_por_especialidad(self, especialidad: str) -> List[Entrenador]:
        """Buscar entrenadores por especialidad"""
        return self.dao.find_by_especialidad(especialidad)
    
    def buscar_por_club(self, club: str) -> List[Entrenador]:
        """Buscar entrenadores por club"""
        return self.dao.find_by_club(club)


# Instancia singleton para compatibilidad
_controller = EntrenadorController()

# Métodos estáticos para compatibilidad hacia atrás
crear_entrenador = lambda data: _controller.crear_entrenador(data)
obtener_entrenador = lambda id: _controller.obtener_entrenador(id)
obtener_entrenador_por_usuario = lambda id: _controller.obtener_entrenador_por_usuario(id)
listar_entrenadores = lambda: _controller.listar_entrenadores()
actualizar_entrenador = lambda id, data: _controller.actualizar_entrenador(id, data)
eliminar_entrenador = lambda id: _controller.eliminar_entrenador(id)
asignar_grupo = lambda e_id, g_id: _controller.asignar_grupo(e_id, g_id)
remover_grupo = lambda e_id, g_id: _controller.remover_grupo(e_id, g_id)
obtener_grupos_entrenador = lambda id: _controller.obtener_grupos_entrenador(id)
buscar_entrenadores = lambda c: _controller.buscar_entrenadores(c)
