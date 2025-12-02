"""
Utilidad para respuestas de API estandarizadas
TODO: Implementar la clase ApiResponse
"""


class ApiResponse:
    """Clase para estandarizar respuestas de la API"""
    
    @staticmethod
    def success(data=None, message: str = "Operación exitosa", status_code: int = 200):
        """Respuesta exitosa"""
        # TODO: Implementar
        pass
    
    @staticmethod
    def error(message: str = "Error en la operación", status_code: int = 400, errors=None):
        """Respuesta de error"""
        # TODO: Implementar
        pass
    
    @staticmethod
    def not_found(message: str = "Recurso no encontrado"):
        """Respuesta de recurso no encontrado"""
        # TODO: Implementar
        pass
    
    @staticmethod
    def created(data=None, message: str = "Recurso creado exitosamente"):
        """Respuesta de recurso creado"""
        # TODO: Implementar
        pass
    
    @staticmethod
    def deleted(message: str = "Recurso eliminado exitosamente"):
        """Respuesta de recurso eliminado"""
        # TODO: Implementar
        pass
