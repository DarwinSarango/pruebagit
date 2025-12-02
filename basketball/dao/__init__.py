"""
Data Access Object (DAO) Package
Proporciona una capa de abstracción para el acceso a datos
"""

from .generic_dao import GenericDAO, ModelDAO
from .model_daos import (
    UsuarioDAO,
    GrupoAtletaDAO,
    AtletaDAO,
    InscripcionDAO,
    PruebaAntropometricaDAO,
    PruebaFisicaDAO,
    EntrenadorDAO,
    EstudianteVinculacionDAO,
)

__all__ = [
    'GenericDAO',
    'ModelDAO',
    'UsuarioDAO',
    'GrupoAtletaDAO',
    'AtletaDAO',
    'InscripcionDAO',
    'PruebaAntropometricaDAO',
    'PruebaFisicaDAO',
    'EntrenadorDAO',
    'EstudianteVinculacionDAO',
]
