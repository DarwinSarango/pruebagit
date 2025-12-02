"""
Comando para poblar la base de datos con datos de prueba
TODO: Implementar la lógica para crear datos de prueba
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos'

    def handle(self, *args, **options):
        # TODO: Implementar la creación de datos de prueba
        self.stdout.write(self.style.WARNING('Comando seed_data no implementado'))
        self.stdout.write(self.style.NOTICE('TODO: Crear datos de prueba para:'))
        self.stdout.write('  - Usuarios')
        self.stdout.write('  - Grupos de Atletas')
        self.stdout.write('  - Atletas')
        self.stdout.write('  - Inscripciones')
        self.stdout.write('  - Pruebas Antropométricas')
        self.stdout.write('  - Pruebas Físicas')
        self.stdout.write('  - Entrenadores')
        self.stdout.write('  - Estudiantes de Vinculación')
