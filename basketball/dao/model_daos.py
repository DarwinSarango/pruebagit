"""
DAOs específicos para los modelos del módulo Basketball
"""

from django.db.models import Q, Avg, Count
from typing import List, Optional, Dict, Any

from .generic_dao import GenericDAO, ModelDAO
from basketball.models import (
    Usuario, Atleta, GrupoAtleta, Inscripcion,
    PruebaAntropometrica, PruebaFisica, Entrenador, EstudianteVinculacion
)


class UsuarioDAO(ModelDAO[Usuario]):
    """DAO específico para Usuario"""
    
    def __init__(self):
        super().__init__(Usuario)
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Buscar usuario por email"""
        return self.find_by_field('email', email)
    
    def find_by_dni(self, dni: str) -> Optional[Usuario]:
        """Buscar usuario por DNI"""
        return self.find_by_field('dni', dni)
    
    def find_by_rol(self, rol: str) -> List[Usuario]:
        """Buscar usuarios por rol"""
        return list(self.find_by_filters({'rol': rol}, active_only=True))
    
    def find_administradores(self) -> List[Usuario]:
        """Obtener todos los administradores"""
        return self.find_by_rol('ADMINISTRADOR')
    
    def find_entrenadores(self) -> List[Usuario]:
        """Obtener todos los usuarios con rol entrenador"""
        return self.find_by_rol('ENTRENADOR')


class GrupoAtletaDAO(ModelDAO[GrupoAtleta]):
    """DAO específico para GrupoAtleta"""
    
    def __init__(self):
        super().__init__(GrupoAtleta)
    
    def find_by_nombre(self, nombre: str) -> Optional[GrupoAtleta]:
        """Buscar grupo por nombre"""
        return self.find_by_field('nombre', nombre)
    
    def find_by_categoria(self, categoria: str) -> List[GrupoAtleta]:
        """Buscar grupos por categoría"""
        return list(self.find_by_filters({'categoria': categoria}, active_only=True))
    
    def find_by_edad(self, edad: int) -> List[GrupoAtleta]:
        """Buscar grupos que acepten una edad específica"""
        return list(self.find_all(active_only=True).filter(
            rango_edad_minima__lte=edad,
            rango_edad_maxima__gte=edad
        ))
    
    def get_grupos_con_atletas(self) -> List[Dict[str, Any]]:
        """Obtener grupos con conteo de atletas"""
        return list(
            self.find_all(active_only=True)
            .annotate(total_atletas=Count('atletas'))
            .values('id', 'nombre', 'categoria', 'total_atletas')
        )


class AtletaDAO(ModelDAO[Atleta]):
    """DAO específico para Atleta"""
    
    def __init__(self):
        super().__init__(Atleta)
    
    def find_by_dni(self, dni: str) -> Optional[Atleta]:
        """Buscar atleta por DNI"""
        return self.find_by_field('dni', dni)
    
    def find_by_grupo(self, grupo_id: int) -> List[Atleta]:
        """Buscar atletas por grupo"""
        return list(self.find_by_filters({'grupo_id': grupo_id}, active_only=True))
    
    def find_by_sexo(self, sexo: str) -> List[Atleta]:
        """Buscar atletas por sexo"""
        return list(self.find_by_filters({'sexo': sexo}, active_only=True))
    
    def find_by_rango_edad(self, edad_min: int, edad_max: int) -> List[Atleta]:
        """Buscar atletas por rango de edad"""
        return list(self.find_all(active_only=True).filter(
            edad__gte=edad_min,
            edad__lte=edad_max
        ))
    
    def search(self, criterios: Dict[str, Any]) -> List[Atleta]:
        """Buscar atletas con criterios avanzados"""
        queryset = self.find_all(active_only=True)
        
        if criterios.get('nombre'):
            queryset = queryset.filter(nombre_atleta__icontains=criterios['nombre'])
        if criterios.get('apellido'):
            queryset = queryset.filter(apellido_atleta__icontains=criterios['apellido'])
        if criterios.get('grupo_id'):
            queryset = queryset.filter(grupo_id=criterios['grupo_id'])
        if criterios.get('sexo'):
            queryset = queryset.filter(sexo=criterios['sexo'])
        if criterios.get('edad_min'):
            queryset = queryset.filter(edad__gte=criterios['edad_min'])
        if criterios.get('edad_max'):
            queryset = queryset.filter(edad__lte=criterios['edad_max'])
        
        return list(queryset)
    
    def find_sin_grupo(self) -> List[Atleta]:
        """Obtener atletas sin grupo asignado"""
        return list(self.find_by_filters({'grupo': None}, active_only=True))
    
    def asignar_grupo(self, atleta_id: int, grupo_id: int) -> Optional[Atleta]:
        """Asignar un grupo a un atleta"""
        return self.update(atleta_id, grupo_id=grupo_id)


class InscripcionDAO(ModelDAO[Inscripcion]):
    """DAO específico para Inscripcion"""
    
    def __init__(self):
        super().__init__(Inscripcion)
        self._soft_delete_field = 'habilitada'  # Usar habilitada como soft delete
    
    def find_by_atleta(self, atleta_id: int) -> List[Inscripcion]:
        """Buscar inscripciones de un atleta"""
        return list(self.find_by_filters({'atleta_id': atleta_id}))
    
    def find_by_tipo(self, tipo: str) -> List[Inscripcion]:
        """Buscar inscripciones por tipo"""
        return list(self.find_by_filters({'tipo_inscripcion': tipo}))
    
    def find_habilitadas(self) -> List[Inscripcion]:
        """Obtener inscripciones habilitadas"""
        return list(self.find_by_filters({'habilitada': True}))
    
    def find_pendientes(self) -> List[Inscripcion]:
        """Obtener inscripciones pendientes de habilitar"""
        return list(self.find_by_filters({'habilitada': False}))
    
    def habilitar(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Habilitar una inscripción"""
        return self.update(inscripcion_id, habilitada=True)
    
    def deshabilitar(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Deshabilitar una inscripción"""
        return self.update(inscripcion_id, habilitada=False)
    
    def tiene_inscripcion_activa(self, atleta_id: int) -> bool:
        """Verificar si un atleta tiene inscripción activa"""
        return self.model_class.objects.filter(
            atleta_id=atleta_id,
            habilitada=True
        ).exists()


class PruebaAntropometricaDAO(ModelDAO[PruebaAntropometrica]):
    """DAO específico para PruebaAntropometrica"""
    
    def __init__(self):
        super().__init__(PruebaAntropometrica)
    
    def find_by_atleta(self, atleta_id: int) -> List[PruebaAntropometrica]:
        """Buscar pruebas de un atleta"""
        return list(
            self.find_by_filters({'atleta_id': atleta_id}, active_only=True)
            .order_by('-fecha_registro')
        )
    
    def find_ultima_by_atleta(self, atleta_id: int) -> Optional[PruebaAntropometrica]:
        """Obtener la última prueba de un atleta"""
        return (
            self.find_all(active_only=True)
            .filter(atleta_id=atleta_id)
            .order_by('-fecha_registro')
            .first()
        )
    
    def get_promedio_imc_by_grupo(self, grupo_id: int) -> Optional[float]:
        """Obtener promedio de IMC de un grupo"""
        result = (
            self.model_class.objects
            .filter(atleta__grupo_id=grupo_id, estado=True)
            .aggregate(promedio=Avg('indice_masa_corporal'))
        )
        return result.get('promedio')
    
    def get_estadisticas_by_atleta(self, atleta_id: int) -> Dict[str, Any]:
        """Obtener estadísticas antropométricas de un atleta"""
        pruebas = self.find_by_atleta(atleta_id)
        if not pruebas:
            return {}
        
        return {
            'total_pruebas': len(pruebas),
            'ultima_prueba': pruebas[0] if pruebas else None,
            'promedio_imc': sum(p.indice_masa_corporal or 0 for p in pruebas) / len(pruebas),
            'promedio_peso': sum(p.peso for p in pruebas) / len(pruebas),
            'promedio_estatura': sum(p.estatura for p in pruebas) / len(pruebas),
        }


class PruebaFisicaDAO(ModelDAO[PruebaFisica]):
    """DAO específico para PruebaFisica"""
    
    def __init__(self):
        super().__init__(PruebaFisica)
    
    def find_by_atleta(self, atleta_id: int) -> List[PruebaFisica]:
        """Buscar pruebas de un atleta"""
        return list(
            self.find_by_filters({'atleta_id': atleta_id}, active_only=True)
            .order_by('-fecha_registro')
        )
    
    def find_by_tipo(self, tipo_prueba: str) -> List[PruebaFisica]:
        """Buscar pruebas por tipo"""
        return list(self.find_by_filters({'tipo_prueba': tipo_prueba}, active_only=True))
    
    def find_by_atleta_y_tipo(self, atleta_id: int, tipo_prueba: str) -> List[PruebaFisica]:
        """Buscar pruebas de un atleta por tipo"""
        return list(
            self.find_by_filters(
                {'atleta_id': atleta_id, 'tipo_prueba': tipo_prueba},
                active_only=True
            ).order_by('-fecha_registro')
        )
    
    def find_ultima_by_atleta_y_tipo(
        self, atleta_id: int, tipo_prueba: str
    ) -> Optional[PruebaFisica]:
        """Obtener la última prueba de un atleta por tipo"""
        pruebas = self.find_by_atleta_y_tipo(atleta_id, tipo_prueba)
        return pruebas[0] if pruebas else None
    
    def get_promedio_by_tipo(self, tipo_prueba: str) -> Optional[float]:
        """Obtener promedio de resultados por tipo de prueba"""
        result = (
            self.model_class.objects
            .filter(tipo_prueba=tipo_prueba, estado=True)
            .aggregate(promedio=Avg('resultado'))
        )
        return result.get('promedio')
    
    def get_estadisticas_by_atleta(self, atleta_id: int) -> Dict[str, Any]:
        """Obtener estadísticas físicas de un atleta"""
        from basketball.models import TipoPrueba
        
        estadisticas = {}
        for tipo_choice in TipoPrueba.choices:
            tipo = tipo_choice[0]
            pruebas = self.find_by_atleta_y_tipo(atleta_id, tipo)
            if pruebas:
                estadisticas[tipo] = {
                    'total_pruebas': len(pruebas),
                    'ultimo_resultado': pruebas[0].resultado,
                    'mejor_resultado': max(p.resultado for p in pruebas),
                    'promedio': sum(p.resultado for p in pruebas) / len(pruebas),
                }
        
        return estadisticas


class EntrenadorDAO(ModelDAO[Entrenador]):
    """DAO específico para Entrenador"""
    
    def __init__(self):
        super().__init__(Entrenador)
        self._soft_delete_field = None  # No tiene campo de estado
    
    def find_by_usuario(self, usuario_id: int) -> Optional[Entrenador]:
        """Buscar entrenador por usuario"""
        return self.find_by_field('usuario_id', usuario_id)
    
    def find_by_especialidad(self, especialidad: str) -> List[Entrenador]:
        """Buscar entrenadores por especialidad"""
        return list(self.find_by_criteria({'especialidad__icontains': especialidad}))
    
    def find_by_club(self, club: str) -> List[Entrenador]:
        """Buscar entrenadores por club"""
        return list(self.find_by_filters({'club_asignado': club}))
    
    def find_by_grupo(self, grupo_id: int) -> List[Entrenador]:
        """Buscar entrenadores asignados a un grupo"""
        return list(self.find_all().filter(grupos__id=grupo_id))
    
    def asignar_grupo(self, entrenador_id: int, grupo_id: int) -> Optional[Entrenador]:
        """Asignar un grupo a un entrenador"""
        entrenador = self.find_by_id(entrenador_id)
        if entrenador:
            from basketball.models import GrupoAtleta
            grupo = GrupoAtleta.objects.filter(id=grupo_id).first()
            if grupo:
                entrenador.grupos.add(grupo)
                return entrenador
        return None
    
    def remover_grupo(self, entrenador_id: int, grupo_id: int) -> Optional[Entrenador]:
        """Remover un grupo de un entrenador"""
        entrenador = self.find_by_id(entrenador_id)
        if entrenador:
            entrenador.grupos.remove(grupo_id)
            return entrenador
        return None
    
    def get_grupos(self, entrenador_id: int) -> List:
        """Obtener grupos de un entrenador"""
        entrenador = self.find_by_id(entrenador_id)
        if entrenador:
            return list(entrenador.grupos.all())
        return []


class EstudianteVinculacionDAO(ModelDAO[EstudianteVinculacion]):
    """DAO específico para EstudianteVinculacion"""
    
    def __init__(self):
        super().__init__(EstudianteVinculacion)
        self._soft_delete_field = None  # No tiene campo de estado
    
    def find_by_usuario(self, usuario_id: int) -> Optional[EstudianteVinculacion]:
        """Buscar estudiante por usuario"""
        return self.find_by_field('usuario_id', usuario_id)
    
    def find_by_carrera(self, carrera: str) -> List[EstudianteVinculacion]:
        """Buscar estudiantes por carrera"""
        return list(self.find_by_criteria({'carrera__icontains': carrera}))
    
    def find_by_semestre(self, semestre: str) -> List[EstudianteVinculacion]:
        """Buscar estudiantes por semestre"""
        return list(self.find_by_criteria({'semestre__icontains': semestre}))
