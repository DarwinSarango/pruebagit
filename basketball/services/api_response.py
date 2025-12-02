"""
Clase base para respuestas de API
Maneja códigos de estado, mensajes y data
"""

from typing import Any, Optional
from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """Clase para estandarizar las respuestas de la API"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operación exitosa",
        status_code: int = status.HTTP_200_OK
    ) -> Response:
        """Respuesta exitosa"""
        return Response({
            "status": "success",
            "code": status_code,
            "message": message,
            "data": data
        }, status=status_code)
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "Recurso creado exitosamente"
    ) -> Response:
        """Respuesta de recurso creado"""
        return Response({
            "status": "success",
            "code": status.HTTP_201_CREATED,
            "message": message,
            "data": data
        }, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def error(
        message: str = "Error en la operación",
        errors: Any = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """Respuesta de error"""
        return Response({
            "status": "error",
            "code": status_code,
            "message": message,
            "errors": errors
        }, status=status_code)
    
    @staticmethod
    def not_found(
        message: str = "Recurso no encontrado",
        resource: Optional[str] = None
    ) -> Response:
        """Respuesta de recurso no encontrado"""
        return Response({
            "status": "error",
            "code": status.HTTP_404_NOT_FOUND,
            "message": message,
            "resource": resource
        }, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(
        message: str = "No autorizado"
    ) -> Response:
        """Respuesta de no autorizado"""
        return Response({
            "status": "error",
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": message
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(
        message: str = "Acceso denegado"
    ) -> Response:
        """Respuesta de acceso denegado"""
        return Response({
            "status": "error",
            "code": status.HTTP_403_FORBIDDEN,
            "message": message
        }, status=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def validation_error(
        errors: Any,
        message: str = "Error de validación"
    ) -> Response:
        """Respuesta de error de validación"""
        return Response({
            "status": "error",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": message,
            "errors": errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    @staticmethod
    def server_error(
        message: str = "Error interno del servidor",
        details: Optional[str] = None
    ) -> Response:
        """Respuesta de error del servidor"""
        return Response({
            "status": "error",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": message,
            "details": details
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def no_content(
        message: str = "Sin contenido"
    ) -> Response:
        """Respuesta sin contenido"""
        return Response({
            "status": "success",
            "code": status.HTTP_204_NO_CONTENT,
            "message": message
        }, status=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def paginated(
        data: Any,
        page: int,
        total_pages: int,
        total_items: int,
        message: str = "Lista obtenida exitosamente"
    ) -> Response:
        """Respuesta paginada"""
        return Response({
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": message,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items
            }
        }, status=status.HTTP_200_OK)
