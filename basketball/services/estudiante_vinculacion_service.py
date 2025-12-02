"""
Servicio API para Estudiantes de Vinculación - Usando DAO
"""

from basketball.controllers.estudiante_vinculacion_controller import EstudianteVinculacionController
from basketball.services.api_response import APIResponse
from basketball.serializers import EstudianteVinculacionSerializer


class EstudianteVinculacionService:
    """Servicio para operaciones de Estudiantes de Vinculación a través de API"""
    
    _controller = EstudianteVinculacionController()
    
    @classmethod
    def crear_estudiante(cls, data: dict):
        """Crear un nuevo estudiante de vinculación"""
        try:
            estudiante = cls._controller.crear_estudiante(data)
            serializer = EstudianteVinculacionSerializer(estudiante)
            return APIResponse.created(
                data=serializer.data,
                message="Estudiante de vinculación creado exitosamente"
            )
        except Exception as e:
            return APIResponse.error(
                message="Error al crear estudiante de vinculación",
                errors=str(e)
            )
    
    @classmethod
    def obtener_estudiante(cls, estudiante_id: int):
        """Obtener un estudiante por ID"""
        estudiante = cls._controller.obtener_estudiante(estudiante_id)
        if estudiante:
            serializer = EstudianteVinculacionSerializer(estudiante)
            return APIResponse.success(
                data=serializer.data,
                message="Estudiante encontrado"
            )
        return APIResponse.not_found(
            message="Estudiante no encontrado",
            resource=f"Estudiante con ID {estudiante_id}"
        )
    
    @classmethod
    def obtener_estudiante_por_usuario(cls, usuario_id: int):
        """Obtener un estudiante por ID de usuario"""
        estudiante = cls._controller.obtener_estudiante_por_usuario(usuario_id)
        if estudiante:
            serializer = EstudianteVinculacionSerializer(estudiante)
            return APIResponse.success(
                data=serializer.data,
                message="Estudiante encontrado"
            )
        return APIResponse.not_found(
            message="Estudiante no encontrado para este usuario"
        )
    
    @classmethod
    def listar_estudiantes(cls):
        """Listar todos los estudiantes"""
        estudiantes = cls._controller.listar_estudiantes()
        serializer = EstudianteVinculacionSerializer(estudiantes, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(estudiantes)} estudiantes"
        )
    
    @classmethod
    def actualizar_estudiante(cls, estudiante_id: int, data: dict):
        """Actualizar un estudiante"""
        estudiante = cls._controller.actualizar_estudiante(estudiante_id, data)
        if estudiante:
            serializer = EstudianteVinculacionSerializer(estudiante)
            return APIResponse.success(
                data=serializer.data,
                message="Estudiante actualizado exitosamente"
            )
        return APIResponse.not_found(
            message="Estudiante no encontrado",
            resource=f"Estudiante con ID {estudiante_id}"
        )
    
    @classmethod
    def eliminar_estudiante(cls, estudiante_id: int):
        """Eliminar un estudiante"""
        if cls._controller.eliminar_estudiante(estudiante_id):
            return APIResponse.success(
                message="Estudiante eliminado exitosamente"
            )
        return APIResponse.not_found(
            message="Estudiante no encontrado",
            resource=f"Estudiante con ID {estudiante_id}"
        )
    
    @classmethod
    def buscar_estudiantes(cls, criterios: dict):
        """Buscar estudiantes por criterios"""
        estudiantes = cls._controller.buscar_estudiantes(criterios)
        serializer = EstudianteVinculacionSerializer(estudiantes, many=True)
        return APIResponse.success(
            data=serializer.data,
            message=f"Se encontraron {len(estudiantes)} estudiantes"
        )
