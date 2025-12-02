"""
Modelos del módulo Basketball
TODO: Implementar los modelos según el diagrama de clases

Modelos a implementar:
- Usuario
- Atleta
- GrupoAtleta
- Inscripcion
- PruebaAntropometrica
- PruebaFisica
- Entrenador
- EstudianteVinculacion
"""

from django.db import models


# TODO: Implementar TipoInscripcion (Enum/TextChoices)
class TipoInscripcion(models.TextChoices):
    """Enum para tipos de inscripción"""
    pass


# TODO: Implementar TipoPrueba (Enum/TextChoices)
class TipoPrueba(models.TextChoices):
    """Enum para tipos de prueba física"""
    pass


# TODO: Implementar modelo Usuario
class Usuario(models.Model):
    """
    Modelo Usuario
    Atributos según diagrama:
    - id: Int
    - nombre: String
    - apellido: String
    - email: String
    - clave: String
    - fotoPerfil: String
    - dni: String
    - rol: String
    - estado: Boolean
    - fechaRegistro: Date
    """
    pass


# TODO: Implementar modelo GrupoAtleta
class GrupoAtleta(models.Model):
    """
    Modelo GrupoAtleta
    Atributos según diagrama:
    - id: Int
    - nombre: String
    - rangoEdadMinima: Integer
    - rangoEdadMaxima: Integer
    - categoria: String
    - fechaCreacion: Date
    - estado: Boolean
    """
    pass


# TODO: Implementar modelo Entrenador
class Entrenador(models.Model):
    """
    Modelo Entrenador (hereda de Usuario)
    Atributos según diagrama:
    - especialidad: String
    - clubAsignado: String
    """
    pass


# TODO: Implementar modelo EstudianteVinculacion
class EstudianteVinculacion(models.Model):
    """
    Modelo EstudianteVinculacion (hereda de Usuario)
    Atributos según diagrama:
    - carrera: String
    - semestre: String
    """
    pass


# TODO: Implementar modelo Atleta
class Atleta(models.Model):
    """
    Modelo Atleta
    Atributos según diagrama:
    - nombreAtleta: String
    - apellidoAtleta: String
    - dni: String
    - fechaNacimiento: Date
    - edad: Integer
    - sexo: String
    - email: String
    - telefono: String
    - tipoSangre: String
    - datosRepresentante: String
    - telefonoRepresentante: String
    """
    pass


# TODO: Implementar modelo Inscripcion
class Inscripcion(models.Model):
    """
    Modelo Inscripcion
    Atributos según diagrama:
    - id: Int
    - fechaInscripcion: Date
    - tipoInscripcion: Enum
    - fechaCreación: Date
    - habilitada: Boolean
    """
    pass


# TODO: Implementar modelo PruebaAntropometrica
class PruebaAntropometrica(models.Model):
    """
    Modelo PruebaAntropometrica
    Atributos según diagrama:
    - id: Int
    - fechaRegistro: Date
    - indiceMasaCorporal: Float
    - estatura: Float
    - alturaSentado: Float
    - envergadura: Float
    - indiceCornico: Float
    - observaciones: String
    - estado: Boolean
    """
    pass


# TODO: Implementar modelo PruebaFisica
class PruebaFisica(models.Model):
    """
    Modelo PruebaFisica
    Atributos según diagrama:
    - id: Int
    - fechaRegistro: Date
    - tipoPrueba: Enum
    - resultado: Float
    - unidadMedida: String
    - observaciones: String
    - estado: Boolean
    """
    pass
