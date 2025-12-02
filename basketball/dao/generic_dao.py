"""
DAO Genérico para operaciones CRUD
Proporciona una capa de abstracción reutilizable para el acceso a datos
"""

from typing import TypeVar, Generic, List, Optional, Dict, Any, Type
from django.db import models, transaction
from django.db.models import QuerySet, Q
from django.core.exceptions import ObjectDoesNotExist

# TypeVar para el modelo genérico
T = TypeVar('T', bound=models.Model)


class GenericDAO(Generic[T]):
    """
    DAO Genérico que proporciona operaciones CRUD estándar para cualquier modelo Django.
    
    Uso:
        class AtletaDAO(GenericDAO[Atleta]):
            def __init__(self):
                super().__init__(Atleta)
        
        # O directamente:
        dao = GenericDAO(Atleta)
        atletas = dao.find_all()
    """
    
    def __init__(self, model_class: Type[T]):
        """
        Inicializa el DAO con la clase del modelo.
        
        Args:
            model_class: Clase del modelo Django
        """
        self.model_class = model_class
        self._soft_delete_field = 'estado'  # Campo para soft delete
    
    # ==================== CREATE ====================
    
    def create(self, **kwargs) -> T:
        """
        Crear una nueva instancia del modelo.
        
        Args:
            **kwargs: Campos del modelo
            
        Returns:
            Instancia creada del modelo
        """
        with transaction.atomic():
            instance = self.model_class.objects.create(**kwargs)
            return instance
    
    def create_from_dict(self, data: Dict[str, Any]) -> T:
        """
        Crear una instancia desde un diccionario.
        
        Args:
            data: Diccionario con los datos del modelo
            
        Returns:
            Instancia creada del modelo
        """
        return self.create(**data)
    
    def bulk_create(self, instances: List[Dict[str, Any]]) -> List[T]:
        """
        Crear múltiples instancias en una sola operación.
        
        Args:
            instances: Lista de diccionarios con datos
            
        Returns:
            Lista de instancias creadas
        """
        with transaction.atomic():
            objects = [self.model_class(**data) for data in instances]
            return self.model_class.objects.bulk_create(objects)
    
    # ==================== READ ====================
    
    def find_by_id(self, pk: int) -> Optional[T]:
        """
        Buscar por ID/primary key.
        
        Args:
            pk: Primary key
            
        Returns:
            Instancia del modelo o None si no existe
        """
        try:
            return self.model_class.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None
    
    def find_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """
        Buscar por un campo específico.
        
        Args:
            field_name: Nombre del campo
            value: Valor a buscar
            
        Returns:
            Primera instancia encontrada o None
        """
        try:
            return self.model_class.objects.get(**{field_name: value})
        except ObjectDoesNotExist:
            return None
        except self.model_class.MultipleObjectsReturned:
            return self.model_class.objects.filter(**{field_name: value}).first()
    
    def find_all(self, active_only: bool = False) -> QuerySet[T]:
        """
        Obtener todos los registros.
        
        Args:
            active_only: Si es True, solo devuelve registros activos
            
        Returns:
            QuerySet con todos los registros
        """
        queryset = self.model_class.objects.all()
        if active_only and hasattr(self.model_class, self._soft_delete_field):
            queryset = queryset.filter(**{self._soft_delete_field: True})
        return queryset
    
    def find_all_as_list(self, active_only: bool = False) -> List[T]:
        """
        Obtener todos los registros como lista.
        
        Args:
            active_only: Si es True, solo devuelve registros activos
            
        Returns:
            Lista con todos los registros
        """
        return list(self.find_all(active_only))
    
    def find_by_filters(self, filters: Dict[str, Any], active_only: bool = False) -> QuerySet[T]:
        """
        Buscar con filtros exactos.
        
        Args:
            filters: Diccionario de filtros (campo: valor)
            active_only: Si es True, solo devuelve registros activos
            
        Returns:
            QuerySet filtrado
        """
        queryset = self.find_all(active_only)
        return queryset.filter(**filters)
    
    def find_by_criteria(self, criteria: Dict[str, Any], active_only: bool = False) -> QuerySet[T]:
        """
        Buscar con criterios avanzados (soporta lookups de Django).
        
        Args:
            criteria: Diccionario con criterios (ej: {'nombre__icontains': 'juan'})
            active_only: Si es True, solo devuelve registros activos
            
        Returns:
            QuerySet filtrado
        """
        queryset = self.find_all(active_only)
        q_objects = Q()
        for key, value in criteria.items():
            if value is not None:
                q_objects &= Q(**{key: value})
        return queryset.filter(q_objects)
    
    def find_by_q(self, q_filter: Q, active_only: bool = False) -> QuerySet[T]:
        """
        Buscar usando objetos Q de Django para consultas complejas.
        
        Args:
            q_filter: Objeto Q con la consulta
            active_only: Si es True, solo devuelve registros activos
            
        Returns:
            QuerySet filtrado
        """
        queryset = self.find_all(active_only)
        return queryset.filter(q_filter)
    
    def exists(self, pk: int) -> bool:
        """
        Verificar si existe un registro por ID.
        
        Args:
            pk: Primary key
            
        Returns:
            True si existe, False si no
        """
        return self.model_class.objects.filter(pk=pk).exists()
    
    def exists_by_field(self, field_name: str, value: Any) -> bool:
        """
        Verificar si existe un registro por campo.
        
        Args:
            field_name: Nombre del campo
            value: Valor a buscar
            
        Returns:
            True si existe, False si no
        """
        return self.model_class.objects.filter(**{field_name: value}).exists()
    
    def count(self, active_only: bool = False) -> int:
        """
        Contar registros.
        
        Args:
            active_only: Si es True, solo cuenta registros activos
            
        Returns:
            Número de registros
        """
        return self.find_all(active_only).count()
    
    def count_by_filters(self, filters: Dict[str, Any]) -> int:
        """
        Contar registros que coincidan con los filtros.
        
        Args:
            filters: Diccionario de filtros
            
        Returns:
            Número de registros
        """
        return self.find_by_filters(filters).count()
    
    # ==================== UPDATE ====================
    
    def update(self, pk: int, **kwargs) -> Optional[T]:
        """
        Actualizar un registro por ID.
        
        Args:
            pk: Primary key
            **kwargs: Campos a actualizar
            
        Returns:
            Instancia actualizada o None si no existe
        """
        instance = self.find_by_id(pk)
        if instance is None:
            return None
        
        with transaction.atomic():
            for field, value in kwargs.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)
            instance.save()
            return instance
    
    def update_from_dict(self, pk: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Actualizar un registro desde un diccionario.
        
        Args:
            pk: Primary key
            data: Diccionario con los campos a actualizar
            
        Returns:
            Instancia actualizada o None si no existe
        """
        return self.update(pk, **data)
    
    def update_field(self, pk: int, field_name: str, value: Any) -> Optional[T]:
        """
        Actualizar un solo campo.
        
        Args:
            pk: Primary key
            field_name: Nombre del campo
            value: Nuevo valor
            
        Returns:
            Instancia actualizada o None si no existe
        """
        return self.update(pk, **{field_name: value})
    
    def bulk_update(self, instances: List[T], fields: List[str]) -> int:
        """
        Actualizar múltiples instancias en una sola operación.
        
        Args:
            instances: Lista de instancias a actualizar
            fields: Lista de campos a actualizar
            
        Returns:
            Número de registros actualizados
        """
        with transaction.atomic():
            return self.model_class.objects.bulk_update(instances, fields)
    
    def update_by_filters(self, filters: Dict[str, Any], updates: Dict[str, Any]) -> int:
        """
        Actualizar múltiples registros que coincidan con los filtros.
        
        Args:
            filters: Filtros para seleccionar registros
            updates: Campos a actualizar
            
        Returns:
            Número de registros actualizados
        """
        with transaction.atomic():
            return self.model_class.objects.filter(**filters).update(**updates)
    
    # ==================== DELETE ====================
    
    def delete(self, pk: int, soft: bool = True) -> bool:
        """
        Eliminar un registro por ID.
        
        Args:
            pk: Primary key
            soft: Si es True, realiza soft delete (cambia estado a False)
            
        Returns:
            True si se eliminó, False si no existe
        """
        instance = self.find_by_id(pk)
        if instance is None:
            return False
        
        with transaction.atomic():
            if soft and hasattr(instance, self._soft_delete_field):
                setattr(instance, self._soft_delete_field, False)
                instance.save()
            else:
                instance.delete()
            return True
    
    def hard_delete(self, pk: int) -> bool:
        """
        Eliminar permanentemente un registro.
        
        Args:
            pk: Primary key
            
        Returns:
            True si se eliminó, False si no existe
        """
        return self.delete(pk, soft=False)
    
    def delete_by_filters(self, filters: Dict[str, Any], soft: bool = True) -> int:
        """
        Eliminar múltiples registros que coincidan con los filtros.
        
        Args:
            filters: Filtros para seleccionar registros
            soft: Si es True, realiza soft delete
            
        Returns:
            Número de registros eliminados
        """
        with transaction.atomic():
            queryset = self.model_class.objects.filter(**filters)
            if soft and hasattr(self.model_class, self._soft_delete_field):
                return queryset.update(**{self._soft_delete_field: False})
            else:
                count = queryset.count()
                queryset.delete()
                return count
    
    def restore(self, pk: int) -> Optional[T]:
        """
        Restaurar un registro eliminado con soft delete.
        
        Args:
            pk: Primary key
            
        Returns:
            Instancia restaurada o None si no existe
        """
        if not hasattr(self.model_class, self._soft_delete_field):
            return None
        
        instance = self.find_by_id(pk)
        if instance is None:
            return None
        
        setattr(instance, self._soft_delete_field, True)
        instance.save()
        return instance
    
    # ==================== UTILITIES ====================
    
    def get_or_create(self, defaults: Dict[str, Any] = None, **kwargs) -> tuple[T, bool]:
        """
        Obtener o crear un registro.
        
        Args:
            defaults: Campos adicionales para la creación
            **kwargs: Campos para la búsqueda
            
        Returns:
            Tupla (instancia, created)
        """
        return self.model_class.objects.get_or_create(defaults=defaults, **kwargs)
    
    def update_or_create(self, defaults: Dict[str, Any] = None, **kwargs) -> tuple[T, bool]:
        """
        Actualizar o crear un registro.
        
        Args:
            defaults: Campos para actualizar/crear
            **kwargs: Campos para la búsqueda
            
        Returns:
            Tupla (instancia, created)
        """
        return self.model_class.objects.update_or_create(defaults=defaults, **kwargs)
    
    def first(self, active_only: bool = False) -> Optional[T]:
        """
        Obtener el primer registro.
        
        Args:
            active_only: Si es True, solo considera registros activos
            
        Returns:
            Primera instancia o None
        """
        return self.find_all(active_only).first()
    
    def last(self, active_only: bool = False) -> Optional[T]:
        """
        Obtener el último registro.
        
        Args:
            active_only: Si es True, solo considera registros activos
            
        Returns:
            Última instancia o None
        """
        return self.find_all(active_only).last()
    
    def paginate(
        self, 
        page: int = 1, 
        page_size: int = 10, 
        active_only: bool = False,
        order_by: str = None
    ) -> Dict[str, Any]:
        """
        Obtener registros paginados.
        
        Args:
            page: Número de página (1-indexed)
            page_size: Tamaño de página
            active_only: Si es True, solo considera registros activos
            order_by: Campo para ordenar (prefijo '-' para descendente)
            
        Returns:
            Diccionario con datos de paginación
        """
        queryset = self.find_all(active_only)
        
        if order_by:
            queryset = queryset.order_by(order_by)
        
        total = queryset.count()
        total_pages = (total + page_size - 1) // page_size
        
        start = (page - 1) * page_size
        end = start + page_size
        
        return {
            'data': list(queryset[start:end]),
            'page': page,
            'page_size': page_size,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1,
        }
    
    def select_related(self, *fields) -> QuerySet[T]:
        """
        Obtener registros con relaciones cargadas (optimización).
        
        Args:
            *fields: Campos de relación a cargar
            
        Returns:
            QuerySet con select_related
        """
        return self.model_class.objects.select_related(*fields)
    
    def prefetch_related(self, *fields) -> QuerySet[T]:
        """
        Obtener registros con relaciones prefetched (optimización).
        
        Args:
            *fields: Campos de relación a prefetch
            
        Returns:
            QuerySet con prefetch_related
        """
        return self.model_class.objects.prefetch_related(*fields)
    
    def raw_query(self, query: str, params: List[Any] = None) -> QuerySet[T]:
        """
        Ejecutar una consulta SQL raw.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta
            
        Returns:
            QuerySet con resultados
        """
        return self.model_class.objects.raw(query, params or [])
    
    def aggregate(self, **kwargs) -> Dict[str, Any]:
        """
        Realizar agregaciones.
        
        Args:
            **kwargs: Funciones de agregación (ej: total=Sum('precio'))
            
        Returns:
            Diccionario con resultados de agregación
        """
        return self.model_class.objects.aggregate(**kwargs)
    
    def values(self, *fields, active_only: bool = False) -> QuerySet:
        """
        Obtener solo ciertos campos como diccionarios.
        
        Args:
            *fields: Campos a obtener
            active_only: Si es True, solo considera registros activos
            
        Returns:
            QuerySet de diccionarios
        """
        return self.find_all(active_only).values(*fields)
    
    def values_list(self, *fields, flat: bool = False, active_only: bool = False) -> QuerySet:
        """
        Obtener solo ciertos campos como tuplas o valores.
        
        Args:
            *fields: Campos a obtener
            flat: Si es True y solo hay un campo, devuelve valores planos
            active_only: Si es True, solo considera registros activos
            
        Returns:
            QuerySet de tuplas o valores
        """
        return self.find_all(active_only).values_list(*fields, flat=flat)
    
    def distinct(self, *fields) -> QuerySet[T]:
        """
        Obtener registros distintos.
        
        Args:
            *fields: Campos para aplicar distinct
            
        Returns:
            QuerySet con distinct
        """
        if fields:
            return self.model_class.objects.distinct(*fields)
        return self.model_class.objects.distinct()


# ==================== DAOs Específicos ====================

class ModelDAO(GenericDAO[T]):
    """
    Clase base para DAOs específicos de modelos.
    Extiende GenericDAO con la capacidad de agregar métodos personalizados.
    """
    
    def __init__(self, model_class: Type[T]):
        super().__init__(model_class)
    
    def find_active(self) -> QuerySet[T]:
        """Alias para find_all con active_only=True"""
        return self.find_all(active_only=True)
    
    def find_inactive(self) -> QuerySet[T]:
        """Obtener solo registros inactivos"""
        if hasattr(self.model_class, self._soft_delete_field):
            return self.model_class.objects.filter(**{self._soft_delete_field: False})
        return self.model_class.objects.none()
