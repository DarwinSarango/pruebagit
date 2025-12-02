"""
Conexión a base de datos y utilidades de conexión
"""

from django.db import connection, connections
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Clase para gestionar la conexión a la base de datos"""
    
    @staticmethod
    def check_connection() -> dict:
        """Verificar estado de la conexión a la base de datos"""
        try:
            connection.ensure_connection()
            return {
                "status": "connected",
                "database": connection.settings_dict.get('NAME'),
                "host": connection.settings_dict.get('HOST'),
                "port": connection.settings_dict.get('PORT')
            }
        except OperationalError as e:
            logger.error(f"Error de conexión a la base de datos: {e}")
            return {
                "status": "disconnected",
                "error": str(e)
            }
    
    @staticmethod
    def get_connection_info() -> dict:
        """Obtener información de la conexión actual"""
        return {
            "engine": connection.settings_dict.get('ENGINE'),
            "name": connection.settings_dict.get('NAME'),
            "host": connection.settings_dict.get('HOST'),
            "port": connection.settings_dict.get('PORT'),
            "user": connection.settings_dict.get('USER')
        }
    
    @staticmethod
    def execute_raw_query(query: str, params: list = None) -> list:
        """Ejecutar una consulta SQL raw"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params or [])
                if query.strip().upper().startswith('SELECT'):
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
                return []
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {e}")
            raise


class ConnectionManager:
    """Manager para gestionar múltiples conexiones"""
    
    @staticmethod
    def get_all_connections() -> dict:
        """Obtener información de todas las conexiones configuradas"""
        result = {}
        for alias in connections:
            conn = connections[alias]
            result[alias] = {
                "engine": conn.settings_dict.get('ENGINE'),
                "name": conn.settings_dict.get('NAME'),
                "host": conn.settings_dict.get('HOST'),
            }
        return result
    
    @staticmethod
    def test_connection(alias: str = 'default') -> bool:
        """Probar una conexión específica"""
        try:
            conn = connections[alias]
            conn.ensure_connection()
            return True
        except Exception as e:
            logger.error(f"Error probando conexión {alias}: {e}")
            return False
