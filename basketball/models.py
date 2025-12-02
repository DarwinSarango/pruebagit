"""
Modelos del módulo Basketball
Basado en el diagrama de clases proporcionado
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class TipoInscripcion(models.TextChoices):
    """Enum para tipos de inscripción"""
    NUEVO = 'NUEVO', 'Nuevo'
    RENOVACION = 'RENOVACION', 'Renovación'
    TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'


class TipoPrueba(models.TextChoices):
    """Enum para tipos de prueba física"""
    RESISTENCIA = 'RESISTENCIA', 'Resistencia'
    VELOCIDAD = 'VELOCIDAD', 'Velocidad'
    FUERZA = 'FUERZA', 'Fuerza'
    FLEXIBILIDAD = 'FLEXIBILIDAD', 'Flexibilidad'
    AGILIDAD = 'AGILIDAD', 'Agilidad'
    COORDINACION = 'COORDINACION', 'Coordinación'


class Usuario(models.Model):
    """
    Modelo Usuario - Este modelo representa al usuario del sistema
    NOTA: Este modelo es implementado por otro equipo, pero lo incluimos
    como referencia para las relaciones. Cuando el módulo de usuario esté
    listo, se debe integrar con este.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    clave = models.CharField(max_length=255)
    foto_perfil = models.CharField(max_length=255, blank=True, null=True)
    dni = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def iniciar_sesion(self):
        """Método para iniciar sesión"""
        pass

    def recuperar_contrasena(self):
        """Método para recuperar contraseña"""
        pass

    def actualizar_perfil(self):
        """Método para actualizar perfil"""
        pass

    def cerrar_sesion(self):
        """Método para cerrar sesión"""
        pass

    def crear_cuenta_entrenador(self, usuario):
        """Método para crear cuenta de entrenador"""
        pass

    def actualizar_roles(self, user_id: str, rol: str):
        """Método para actualizar roles"""
        pass

    def dar_de_baja_rol(self, user_id: str):
        """Método para dar de baja un rol"""
        pass

    def visualizar_usuarios(self):
        """Método para visualizar usuarios"""
        pass

    def crear_inscripcion(self, datos, inscripcion):
        """Método para crear inscripción"""
        pass

    def habilitar_inscripcion(self, user_id: str):
        """Método para habilitar inscripción"""
        pass

    def actualizar_inscripcion(self, id: str, datos: dict):
        """Método para actualizar inscripción"""
        pass

    def visualizar_inscripcion(self):
        """Método para visualizar inscripciones"""
        pass

    def es_administrador(self) -> bool:
        """Método para verificar si es administrador"""
        return self.rol == 'ADMINISTRADOR'


class GrupoAtleta(models.Model):
    """Modelo para grupos de atletas"""
    nombre = models.CharField(max_length=100)
    rango_edad_minima = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    rango_edad_maxima = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    categoria = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'grupo_atleta'
        verbose_name = 'Grupo de Atleta'
        verbose_name_plural = 'Grupos de Atletas'

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

    def agregar_atleta(self, atleta):
        """Agregar atleta al grupo"""
        pass

    def eliminar_atleta(self, atleta):
        """Eliminar atleta del grupo"""
        pass

    def listar_atletas(self):
        """Listar atletas del grupo"""
        return self.atletas.filter(estado=True)


class Entrenador(models.Model):
    """Modelo Entrenador - Hereda conceptualmente de Usuario"""
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='entrenador'
    )
    especialidad = models.CharField(max_length=100)
    club_asignado = models.CharField(max_length=100)
    grupos = models.ManyToManyField(
        GrupoAtleta,
        related_name='entrenadores',
        blank=True
    )

    class Meta:
        db_table = 'entrenador'
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'

    def __str__(self):
        return f"Entrenador: {self.usuario.nombre} {self.usuario.apellido}"

    def crear_cuenta_estudiante(self):
        """Crear cuenta de estudiante"""
        pass

    def crear_grupo_atletas(self):
        """Crear grupo de atletas"""
        pass

    def actualizar_grupo_atletas(self):
        """Actualizar grupo de atletas"""
        pass

    def visualizar_grupo_atletas(self):
        """Visualizar grupos de atletas"""
        return self.grupos.all()

    def enviar_notificacion(self):
        """Enviar notificación"""
        pass

    def habilitar_inscripcion(self):
        """Habilitar inscripción"""
        pass

    def deshabilitar_inscripcion(self):
        """Deshabilitar inscripción"""
        pass

    def visualizar_inscripcion(self):
        """Visualizar inscripción"""
        pass

    def registrar_prueba_antropometrica(self):
        """Registrar prueba antropométrica"""
        pass

    def actualizar_prueba_antropometrica(self):
        """Actualizar prueba antropométrica"""
        pass

    def visualizar_prueba_antropometrica(self):
        """Visualizar prueba antropométrica"""
        pass

    def registrar_prueba_fisica(self):
        """Registrar prueba física"""
        pass

    def actualizar_prueba_fisica(self):
        """Actualizar prueba física"""
        pass

    def visualizar_prueba_fisica(self):
        """Visualizar prueba física"""
        pass


class EstudianteVinculacion(models.Model):
    """Modelo Estudiante de Vinculación - Hereda conceptualmente de Usuario"""
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='estudiante_vinculacion'
    )
    carrera = models.CharField(max_length=100)
    semestre = models.CharField(max_length=20)

    class Meta:
        db_table = 'estudiante_vinculacion'
        verbose_name = 'Estudiante de Vinculación'
        verbose_name_plural = 'Estudiantes de Vinculación'

    def __str__(self):
        return f"Estudiante: {self.usuario.nombre} {self.usuario.apellido}"

    def registrar_prueba_antropometrica(self):
        """Registrar prueba antropométrica"""
        pass

    def actualizar_prueba_antropometrica(self):
        """Actualizar prueba antropométrica"""
        pass

    def visualizar_prueba_antropometrica(self):
        """Visualizar prueba antropométrica"""
        pass

    def registrar_prueba_fisica(self):
        """Registrar prueba física"""
        pass

    def actualizar_prueba_fisica(self):
        """Actualizar prueba física"""
        pass

    def visualizar_prueba_fisica(self):
        """Visualizar prueba física"""
        pass


class Atleta(models.Model):
    """Modelo Atleta"""
    nombre_atleta = models.CharField(max_length=100)
    apellido_atleta = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sexo = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_sangre = models.CharField(max_length=10, blank=True, null=True)
    datos_representante = models.CharField(max_length=255, blank=True, null=True)
    telefono_representante = models.CharField(max_length=20, blank=True, null=True)
    grupo = models.ForeignKey(
        GrupoAtleta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='atletas'
    )
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'atleta'
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'

    def __str__(self):
        return f"{self.nombre_atleta} {self.apellido_atleta}"

    def recibir_notificacion(self):
        """Recibir notificación"""
        pass

    def visualizar_reporte(self):
        """Visualizar reporte"""
        pass

    def calcular_edad(self):
        """Calcular edad basada en fecha de nacimiento"""
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular edad automáticamente"""
        self.edad = self.calcular_edad()
        super().save(*args, **kwargs)


class Inscripcion(models.Model):
    """Modelo Inscripción"""
    atleta = models.ForeignKey(
        Atleta,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    fecha_inscripcion = models.DateField()
    tipo_inscripcion = models.CharField(
        max_length=20,
        choices=TipoInscripcion.choices,
        default=TipoInscripcion.NUEVO
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    habilitada = models.BooleanField(default=False)

    class Meta:
        db_table = 'inscripcion'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return f"Inscripción {self.id} - {self.atleta}"

    def habilitar(self):
        """Habilitar inscripción"""
        self.habilitada = True
        self.save()

    def deshabilitar(self):
        """Deshabilitar inscripción"""
        self.habilitada = False
        self.save()

    def validar_documentos(self) -> bool:
        """Validar documentos de inscripción"""
        # Implementar lógica de validación
        return True


class PruebaAntropometrica(models.Model):
    """Modelo Prueba Antropométrica"""
    atleta = models.ForeignKey(
        Atleta,
        on_delete=models.CASCADE,
        related_name='pruebas_antropometricas'
    )
    fecha_registro = models.DateField(auto_now_add=True)
    indice_masa_corporal = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    estatura = models.FloatField(validators=[MinValueValidator(0)])
    altura_sentado = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    envergadura = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    indice_cornico = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    peso = models.FloatField(validators=[MinValueValidator(0)])
    observaciones = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'prueba_antropometrica'
        verbose_name = 'Prueba Antropométrica'
        verbose_name_plural = 'Pruebas Antropométricas'

    def __str__(self):
        return f"Prueba Antropométrica - {self.atleta} ({self.fecha_registro})"

    def calcular_imc(self) -> float:
        """Calcular índice de masa corporal"""
        if self.estatura and self.peso:
            altura_metros = self.estatura / 100  # Convertir cm a metros
            self.indice_masa_corporal = round(self.peso / (altura_metros ** 2), 2)
            return self.indice_masa_corporal
        return 0

    def calcular_indice_cornico(self) -> float:
        """Calcular índice córnico"""
        if self.altura_sentado and self.estatura:
            self.indice_cornico = round((self.altura_sentado / self.estatura) * 100, 2)
            return self.indice_cornico
        return 0

    def validar_datos(self) -> bool:
        """Validar datos de la prueba"""
        return self.estatura > 0 and self.peso > 0

    def save(self, *args, **kwargs):
        """Sobrescribir save para calcular IMC e índice córnico"""
        self.calcular_imc()
        self.calcular_indice_cornico()
        super().save(*args, **kwargs)


class PruebaFisica(models.Model):
    """Modelo Prueba Física"""
    atleta = models.ForeignKey(
        Atleta,
        on_delete=models.CASCADE,
        related_name='pruebas_fisicas'
    )
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_prueba = models.CharField(
        max_length=20,
        choices=TipoPrueba.choices
    )
    resultado = models.FloatField()
    unidad_medida = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'prueba_fisica'
        verbose_name = 'Prueba Física'
        verbose_name_plural = 'Pruebas Físicas'

    def __str__(self):
        return f"Prueba {self.tipo_prueba} - {self.atleta} ({self.fecha_registro})"

    def validar_resultado(self) -> bool:
        """Validar resultado de la prueba"""
        return self.resultado >= 0

    def comparar_resultados(self, otra_prueba) -> dict:
        """Comparar resultados con otra prueba"""
        if self.tipo_prueba != otra_prueba.tipo_prueba:
            return {"error": "No se pueden comparar pruebas de diferente tipo"}
        
        diferencia = self.resultado - otra_prueba.resultado
        porcentaje = (diferencia / otra_prueba.resultado) * 100 if otra_prueba.resultado != 0 else 0
        
        return {
            "prueba_actual": self.resultado,
            "prueba_comparada": otra_prueba.resultado,
            "diferencia": round(diferencia, 2),
            "porcentaje_cambio": round(porcentaje, 2)
        }
