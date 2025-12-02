"""
Controladores para Estudiante de Vinculación - Usando DAO Genérico
"""

from typing import List, Optional, Dict, Any

from basketball.models import EstudianteVinculacion, Usuario
from basketball.dao import EstudianteVinculacionDAO, UsuarioDAO


class EstudianteVinculacionController:
    """Controlador para gestionar operaciones de Estudiantes de Vinculación"""
    
    def __init__(self):
        self.dao = EstudianteVinculacionDAO()
        self.usuario_dao = UsuarioDAO()
    
    def crear_estudiante(self, data: dict) -> EstudianteVinculacion:
        """Crear un nuevo estudiante de vinculación"""
        # Procesar usuario
        if 'usuario_id' in data:
            usuario_id = data.pop('usuario_id')
            data['usuario'] = self.usuario_dao.find_by_id(usuario_id)
        
        return self.dao.create_from_dict(data)
    
    def obtener_estudiante(self, estudiante_id: int) -> Optional[EstudianteVinculacion]:
        """Obtener un estudiante por ID"""
        return self.dao.find_by_id(estudiante_id)
    
    def obtener_estudiante_por_usuario(self, usuario_id: int) -> Optional[EstudianteVinculacion]:
        """Obtener un estudiante por ID de usuario"""
        return self.dao.find_by_usuario(usuario_id)
    
    def listar_estudiantes(self) -> List[EstudianteVinculacion]:
        """Listar todos los estudiantes"""
        return list(self.dao.find_all().filter(usuario__estado=True))
    
    def actualizar_estudiante(self, estudiante_id: int, data: dict) -> Optional[EstudianteVinculacion]:
        """Actualizar un estudiante existente"""
        return self.dao.update_from_dict(estudiante_id, data)
    
    def eliminar_estudiante(self, estudiante_id: int) -> bool:
        """Eliminar un estudiante"""
        return self.dao.hard_delete(estudiante_id)
    
    def buscar_estudiantes(self, criterios: dict) -> List[EstudianteVinculacion]:
        """Buscar estudiantes por criterios"""
        queryset = self.dao.find_all().filter(usuario__estado=True)
        
        if criterios.get('carrera'):
            queryset = queryset.filter(carrera__icontains=criterios['carrera'])
        if criterios.get('semestre'):
            queryset = queryset.filter(semestre=criterios['semestre'])
        if criterios.get('nombre'):
            queryset = queryset.filter(usuario__nombre__icontains=criterios['nombre'])
        
        return list(queryset)
    
    def buscar_por_carrera(self, carrera: str) -> List[EstudianteVinculacion]:
        """Buscar estudiantes por carrera"""
        return self.dao.find_by_carrera(carrera)
    
    def buscar_por_semestre(self, semestre: str) -> List[EstudianteVinculacion]:
        """Buscar estudiantes por semestre"""
        return self.dao.find_by_semestre(semestre)


# Instancia singleton para compatibilidad
_controller = EstudianteVinculacionController()

# Métodos estáticos para compatibilidad hacia atrás
crear_estudiante = lambda data: _controller.crear_estudiante(data)
obtener_estudiante = lambda id: _controller.obtener_estudiante(id)
obtener_estudiante_por_usuario = lambda id: _controller.obtener_estudiante_por_usuario(id)
listar_estudiantes = lambda: _controller.listar_estudiantes()
actualizar_estudiante = lambda id, data: _controller.actualizar_estudiante(id, data)
eliminar_estudiante = lambda id: _controller.eliminar_estudiante(id)
buscar_estudiantes = lambda c: _controller.buscar_estudiantes(c)
