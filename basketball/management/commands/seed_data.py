"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar con: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from basketball.models import (
    Usuario, GrupoAtleta, Entrenador, EstudianteVinculacion,
    Atleta, Inscripcion, PruebaAntropometrica, PruebaFisica,
    TipoInscripcion, TipoPrueba
)
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para el módulo de Basketball'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            self.clear_data()

        self.stdout.write(self.style.HTTP_INFO('Iniciando población de datos...'))
        
        # Crear datos en orden de dependencias
        usuarios = self.create_usuarios()
        grupos = self.create_grupos()
        entrenadores = self.create_entrenadores(usuarios, grupos)
        estudiantes = self.create_estudiantes_vinculacion(usuarios)
        atletas = self.create_atletas(grupos)
        inscripciones = self.create_inscripciones(atletas)
        pruebas_antropometricas = self.create_pruebas_antropometricas(atletas)
        pruebas_fisicas = self.create_pruebas_fisicas(atletas)

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Datos creados exitosamente:'))
        self.stdout.write(f'  - Usuarios: {len(usuarios)}')
        self.stdout.write(f'  - Grupos de Atletas: {len(grupos)}')
        self.stdout.write(f'  - Entrenadores: {len(entrenadores)}')
        self.stdout.write(f'  - Estudiantes de Vinculación: {len(estudiantes)}')
        self.stdout.write(f'  - Atletas: {len(atletas)}')
        self.stdout.write(f'  - Inscripciones: {len(inscripciones)}')
        self.stdout.write(f'  - Pruebas Antropométricas: {len(pruebas_antropometricas)}')
        self.stdout.write(f'  - Pruebas Físicas: {len(pruebas_fisicas)}')
        self.stdout.write(self.style.SUCCESS('=' * 50))

    def clear_data(self):
        """Eliminar todos los datos existentes"""
        PruebaFisica.objects.all().delete()
        PruebaAntropometrica.objects.all().delete()
        Inscripcion.objects.all().delete()
        Atleta.objects.all().delete()
        EstudianteVinculacion.objects.all().delete()
        Entrenador.objects.all().delete()
        GrupoAtleta.objects.all().delete()
        Usuario.objects.all().delete()
        self.stdout.write(self.style.WARNING('Datos eliminados.'))

    def create_usuarios(self):
        """Crear usuarios de ejemplo"""
        self.stdout.write('Creando usuarios...')
        
        usuarios_data = [
            # Administrador
            {
                'nombre': 'Carlos',
                'apellido': 'Administrador',
                'email': 'admin@basketball.com',
                'clave': 'admin123',
                'dni': '1712345678',
                'rol': 'ADMINISTRADOR',
                'estado': True,
            },
            # Entrenadores
            {
                'nombre': 'Juan',
                'apellido': 'García López',
                'email': 'juan.garcia@basketball.com',
                'clave': 'coach123',
                'dni': '1723456789',
                'rol': 'ENTRENADOR',
                'estado': True,
            },
            {
                'nombre': 'María',
                'apellido': 'Rodríguez Pérez',
                'email': 'maria.rodriguez@basketball.com',
                'clave': 'coach123',
                'dni': '1734567890',
                'rol': 'ENTRENADOR',
                'estado': True,
            },
            {
                'nombre': 'Pedro',
                'apellido': 'Martínez Silva',
                'email': 'pedro.martinez@basketball.com',
                'clave': 'coach123',
                'dni': '1745678901',
                'rol': 'ENTRENADOR',
                'estado': True,
            },
            # Estudiantes de Vinculación
            {
                'nombre': 'Ana',
                'apellido': 'Sánchez Torres',
                'email': 'ana.sanchez@universidad.edu.ec',
                'clave': 'student123',
                'dni': '1756789012',
                'rol': 'ESTUDIANTE_VINCULACION',
                'estado': True,
            },
            {
                'nombre': 'Luis',
                'apellido': 'Fernández Cruz',
                'email': 'luis.fernandez@universidad.edu.ec',
                'clave': 'student123',
                'dni': '1767890123',
                'rol': 'ESTUDIANTE_VINCULACION',
                'estado': True,
            },
            {
                'nombre': 'Sofía',
                'apellido': 'Morales Vega',
                'email': 'sofia.morales@universidad.edu.ec',
                'clave': 'student123',
                'dni': '1778901234',
                'rol': 'ESTUDIANTE_VINCULACION',
                'estado': True,
            },
        ]

        usuarios = []
        for data in usuarios_data:
            usuario, created = Usuario.objects.get_or_create(
                dni=data['dni'],
                defaults=data
            )
            usuarios.append(usuario)
            if created:
                self.stdout.write(f'  ✓ Usuario creado: {usuario.nombre} {usuario.apellido}')

        return usuarios

    def create_grupos(self):
        """Crear grupos de atletas por categorías de edad"""
        self.stdout.write('Creando grupos de atletas...')
        
        grupos_data = [
            {
                'nombre': 'Mini Basketball',
                'rango_edad_minima': 6,
                'rango_edad_maxima': 8,
                'categoria': 'Iniciación',
                'estado': True,
            },
            {
                'nombre': 'Pre-Infantil',
                'rango_edad_minima': 9,
                'rango_edad_maxima': 10,
                'categoria': 'Formación',
                'estado': True,
            },
            {
                'nombre': 'Infantil',
                'rango_edad_minima': 11,
                'rango_edad_maxima': 12,
                'categoria': 'Formación',
                'estado': True,
            },
            {
                'nombre': 'Cadetes',
                'rango_edad_minima': 13,
                'rango_edad_maxima': 14,
                'categoria': 'Desarrollo',
                'estado': True,
            },
            {
                'nombre': 'Juvenil',
                'rango_edad_minima': 15,
                'rango_edad_maxima': 17,
                'categoria': 'Competición',
                'estado': True,
            },
            {
                'nombre': 'Sub-21',
                'rango_edad_minima': 18,
                'rango_edad_maxima': 21,
                'categoria': 'Alto Rendimiento',
                'estado': True,
            },
        ]

        grupos = []
        for data in grupos_data:
            grupo, created = GrupoAtleta.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            grupos.append(grupo)
            if created:
                self.stdout.write(f'  ✓ Grupo creado: {grupo.nombre} ({grupo.rango_edad_minima}-{grupo.rango_edad_maxima} años)')

        return grupos

    def create_entrenadores(self, usuarios, grupos):
        """Crear entrenadores y asignarles grupos"""
        self.stdout.write('Creando entrenadores...')
        
        entrenadores_data = [
            {
                'usuario_email': 'juan.garcia@basketball.com',
                'especialidad': 'Técnica individual y fundamentos',
                'club_asignado': 'Club Deportivo Universidad',
                'grupos_indices': [0, 1, 2],  # Mini, Pre-Infantil, Infantil
            },
            {
                'usuario_email': 'maria.rodriguez@basketball.com',
                'especialidad': 'Preparación física y acondicionamiento',
                'club_asignado': 'Club Deportivo Universidad',
                'grupos_indices': [3, 4],  # Cadetes, Juvenil
            },
            {
                'usuario_email': 'pedro.martinez@basketball.com',
                'especialidad': 'Táctica y estrategia de juego',
                'club_asignado': 'Club Deportivo Universidad',
                'grupos_indices': [4, 5],  # Juvenil, Sub-21
            },
        ]

        entrenadores = []
        for data in entrenadores_data:
            usuario = next((u for u in usuarios if u.email == data['usuario_email']), None)
            if usuario:
                entrenador, created = Entrenador.objects.get_or_create(
                    usuario=usuario,
                    defaults={
                        'especialidad': data['especialidad'],
                        'club_asignado': data['club_asignado'],
                    }
                )
                # Asignar grupos
                for idx in data['grupos_indices']:
                    if idx < len(grupos):
                        entrenador.grupos.add(grupos[idx])
                
                entrenadores.append(entrenador)
                if created:
                    self.stdout.write(f'  ✓ Entrenador creado: {usuario.nombre} {usuario.apellido}')

        return entrenadores

    def create_estudiantes_vinculacion(self, usuarios):
        """Crear estudiantes de vinculación"""
        self.stdout.write('Creando estudiantes de vinculación...')
        
        estudiantes_data = [
            {
                'usuario_email': 'ana.sanchez@universidad.edu.ec',
                'carrera': 'Licenciatura en Educación Física',
                'semestre': '6to Semestre',
            },
            {
                'usuario_email': 'luis.fernandez@universidad.edu.ec',
                'carrera': 'Fisioterapia',
                'semestre': '7mo Semestre',
            },
            {
                'usuario_email': 'sofia.morales@universidad.edu.ec',
                'carrera': 'Nutrición y Dietética',
                'semestre': '5to Semestre',
            },
        ]

        estudiantes = []
        for data in estudiantes_data:
            usuario = next((u for u in usuarios if u.email == data['usuario_email']), None)
            if usuario:
                estudiante, created = EstudianteVinculacion.objects.get_or_create(
                    usuario=usuario,
                    defaults={
                        'carrera': data['carrera'],
                        'semestre': data['semestre'],
                    }
                )
                estudiantes.append(estudiante)
                if created:
                    self.stdout.write(f'  ✓ Estudiante creado: {usuario.nombre} {usuario.apellido}')

        return estudiantes

    def create_atletas(self, grupos):
        """Crear atletas de ejemplo para cada grupo"""
        self.stdout.write('Creando atletas...')
        
        nombres_masculinos = ['Diego', 'Andrés', 'Sebastián', 'Mateo', 'Santiago', 'Daniel', 'Nicolás', 'Gabriel', 'Lucas', 'Emilio']
        nombres_femeninos = ['Valentina', 'Camila', 'Isabella', 'Mariana', 'Luciana', 'Gabriela', 'Paula', 'Andrea', 'Carolina', 'Daniela']
        apellidos = ['González', 'Rodríguez', 'Martínez', 'López', 'García', 'Hernández', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez', 'Díaz', 'Reyes']
        tipos_sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        atletas = []
        dni_counter = 1000000000

        for grupo in grupos:
            # Crear entre 4 y 6 atletas por grupo
            num_atletas = random.randint(4, 6)
            
            for i in range(num_atletas):
                sexo = random.choice(['Masculino', 'Femenino'])
                nombres = nombres_masculinos if sexo == 'Masculino' else nombres_femeninos
                nombre = random.choice(nombres)
                apellido = f"{random.choice(apellidos)} {random.choice(apellidos)}"
                
                # Calcular edad dentro del rango del grupo
                edad = random.randint(grupo.rango_edad_minima, grupo.rango_edad_maxima)
                fecha_nacimiento = date.today() - timedelta(days=edad * 365 + random.randint(0, 364))
                
                dni_counter += 1
                dni = str(dni_counter)
                
                atleta_data = {
                    'nombre_atleta': nombre,
                    'apellido_atleta': apellido,
                    'dni': dni,
                    'fecha_nacimiento': fecha_nacimiento,
                    'edad': edad,
                    'sexo': sexo,
                    'email': f"{nombre.lower()}.{apellido.split()[0].lower()}@email.com",
                    'telefono': f"09{random.randint(10000000, 99999999)}",
                    'tipo_sangre': random.choice(tipos_sangre),
                    'datos_representante': f"Representante de {nombre}",
                    'telefono_representante': f"09{random.randint(10000000, 99999999)}",
                    'grupo': grupo,
                    'estado': True,
                }

                atleta, created = Atleta.objects.get_or_create(
                    dni=dni,
                    defaults=atleta_data
                )
                atletas.append(atleta)
                if created:
                    self.stdout.write(f'  ✓ Atleta creado: {atleta.nombre_atleta} {atleta.apellido_atleta} ({grupo.nombre})')

        return atletas

    def create_inscripciones(self, atletas):
        """Crear inscripciones para los atletas"""
        self.stdout.write('Creando inscripciones...')
        
        inscripciones = []
        
        for atleta in atletas:
            # Determinar tipo de inscripción aleatoriamente
            tipo = random.choice([TipoInscripcion.NUEVO, TipoInscripcion.RENOVACION])
            
            # Fecha de inscripción en los últimos 6 meses
            dias_atras = random.randint(0, 180)
            fecha_inscripcion = date.today() - timedelta(days=dias_atras)
            
            # 80% de inscripciones habilitadas
            habilitada = random.random() < 0.8
            
            inscripcion, created = Inscripcion.objects.get_or_create(
                atleta=atleta,
                tipo_inscripcion=tipo,
                defaults={
                    'fecha_inscripcion': fecha_inscripcion,
                    'habilitada': habilitada,
                }
            )
            inscripciones.append(inscripcion)
            if created:
                estado = "✓" if habilitada else "○"
                self.stdout.write(f'  {estado} Inscripción: {atleta.nombre_atleta} - {tipo}')

        return inscripciones

    def create_pruebas_antropometricas(self, atletas):
        """Crear pruebas antropométricas para los atletas"""
        self.stdout.write('Creando pruebas antropométricas...')
        
        pruebas = []
        
        for atleta in atletas:
            # Crear entre 1 y 3 pruebas por atleta (histórico)
            num_pruebas = random.randint(1, 3)
            
            for i in range(num_pruebas):
                # Fecha de prueba en los últimos 12 meses
                dias_atras = random.randint(0, 365) - (i * 120)  # Espaciadas en el tiempo
                if dias_atras < 0:
                    dias_atras = 0
                
                # Valores basados en la edad del atleta
                edad = atleta.edad
                
                # Estatura aproximada por edad (en cm)
                if edad <= 8:
                    estatura_base = 120 + (edad - 6) * 5
                elif edad <= 12:
                    estatura_base = 130 + (edad - 8) * 6
                elif edad <= 15:
                    estatura_base = 154 + (edad - 12) * 7
                else:
                    estatura_base = 175 + (edad - 15) * 2
                
                estatura = estatura_base + random.uniform(-5, 10)
                
                # Peso aproximado por estatura
                peso_base = (estatura - 100) * 0.9
                peso = peso_base + random.uniform(-5, 10)
                
                # Altura sentado (aproximadamente 52% de la estatura)
                altura_sentado = estatura * 0.52 + random.uniform(-2, 2)
                
                # Envergadura (similar a la estatura, puede ser mayor en atletas)
                envergadura = estatura * random.uniform(0.98, 1.05)
                
                prueba_data = {
                    'atleta': atleta,
                    'estatura': round(estatura, 1),
                    'peso': round(peso, 1),
                    'altura_sentado': round(altura_sentado, 1),
                    'envergadura': round(envergadura, 1),
                    'observaciones': f'Medición #{i+1} del atleta',
                    'estado': True,
                }
                
                prueba = PruebaAntropometrica.objects.create(**prueba_data)
                # Ajustar fecha de registro
                prueba.fecha_registro = date.today() - timedelta(days=dias_atras)
                prueba.save()
                
                pruebas.append(prueba)
        
        self.stdout.write(f'  ✓ {len(pruebas)} pruebas antropométricas creadas')
        return pruebas

    def create_pruebas_fisicas(self, atletas):
        """Crear pruebas físicas para los atletas"""
        self.stdout.write('Creando pruebas físicas...')
        
        pruebas = []
        
        # Definir rangos de resultados por tipo de prueba
        pruebas_config = {
            TipoPrueba.RESISTENCIA: {
                'unidad': 'minutos',
                'rango': (5, 15),  # Test de Cooper (tiempo en 2km)
                'descripcion': 'Test de resistencia aeróbica',
            },
            TipoPrueba.VELOCIDAD: {
                'unidad': 'segundos',
                'rango': (3, 8),  # Sprint 30 metros
                'descripcion': 'Sprint de velocidad 30m',
            },
            TipoPrueba.FUERZA: {
                'unidad': 'repeticiones',
                'rango': (5, 30),  # Flexiones o sentadillas
                'descripcion': 'Test de fuerza muscular',
            },
            TipoPrueba.FLEXIBILIDAD: {
                'unidad': 'centímetros',
                'rango': (-5, 20),  # Sit and reach
                'descripcion': 'Test de flexibilidad sit and reach',
            },
            TipoPrueba.AGILIDAD: {
                'unidad': 'segundos',
                'rango': (8, 18),  # Test de Illinois
                'descripcion': 'Test de agilidad Illinois',
            },
            TipoPrueba.COORDINACION: {
                'unidad': 'puntos',
                'rango': (5, 20),  # Test de coordinación
                'descripcion': 'Test de coordinación óculo-manual',
            },
        }
        
        for atleta in atletas:
            # Cada atleta tiene entre 3 y 6 tipos de pruebas
            tipos_prueba = random.sample(list(TipoPrueba.choices), random.randint(3, 6))
            
            for tipo_choice in tipos_prueba:
                tipo = tipo_choice[0]
                config = pruebas_config[tipo]
                
                # Ajustar resultado según edad (atletas mayores tienden a mejores resultados)
                factor_edad = min(atleta.edad / 18, 1)  # Factor de 0 a 1
                rango_min, rango_max = config['rango']
                
                # Para tiempo (menor es mejor), invertir el factor
                if config['unidad'] in ['segundos', 'minutos']:
                    resultado = rango_max - (rango_max - rango_min) * factor_edad * random.uniform(0.7, 1.0)
                else:
                    resultado = rango_min + (rango_max - rango_min) * factor_edad * random.uniform(0.7, 1.0)
                
                # Fecha de prueba aleatoria en los últimos 6 meses
                dias_atras = random.randint(0, 180)
                
                prueba_data = {
                    'atleta': atleta,
                    'tipo_prueba': tipo,
                    'resultado': round(resultado, 2),
                    'unidad_medida': config['unidad'],
                    'observaciones': config['descripcion'],
                    'estado': True,
                }
                
                prueba = PruebaFisica.objects.create(**prueba_data)
                # Ajustar fecha de registro
                prueba.fecha_registro = date.today() - timedelta(days=dias_atras)
                prueba.save()
                
                pruebas.append(prueba)
        
        self.stdout.write(f'  ✓ {len(pruebas)} pruebas físicas creadas')
        return pruebas
