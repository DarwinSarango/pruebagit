"""
Tests del módulo Basketball
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal

from basketball.models import (
    Usuario, GrupoAtleta, Entrenador, EstudianteVinculacion,
    Atleta, Inscripcion, PruebaAntropometrica, PruebaFisica,
    TipoInscripcion, TipoPrueba
)


class AtletaModelTest(TestCase):
    """Tests para el modelo Atleta"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.grupo = GrupoAtleta.objects.create(
            nombre="Sub-15",
            rango_edad_minima=13,
            rango_edad_maxima=15,
            categoria="Infantil"
        )
        
        self.atleta = Atleta.objects.create(
            nombre_atleta="Juan",
            apellido_atleta="Pérez",
            dni="1234567890",
            fecha_nacimiento=date(2010, 5, 15),
            sexo="Masculino",
            email="juan@example.com",
            telefono="0991234567",
            grupo=self.grupo
        )
    
    def test_atleta_creation(self):
        """Test creación de atleta"""
        self.assertEqual(self.atleta.nombre_atleta, "Juan")
        self.assertEqual(self.atleta.apellido_atleta, "Pérez")
        self.assertTrue(self.atleta.estado)
    
    def test_atleta_str(self):
        """Test representación string de atleta"""
        self.assertEqual(str(self.atleta), "Juan Pérez")
    
    def test_atleta_edad_calculada(self):
        """Test cálculo automático de edad"""
        self.assertIsNotNone(self.atleta.edad)
        self.assertGreater(self.atleta.edad, 0)
    
    def test_atleta_grupo_asignado(self):
        """Test grupo asignado al atleta"""
        self.assertEqual(self.atleta.grupo, self.grupo)


class GrupoAtletaModelTest(TestCase):
    """Tests para el modelo GrupoAtleta"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.grupo = GrupoAtleta.objects.create(
            nombre="Sub-17",
            rango_edad_minima=15,
            rango_edad_maxima=17,
            categoria="Juvenil"
        )
    
    def test_grupo_creation(self):
        """Test creación de grupo"""
        self.assertEqual(self.grupo.nombre, "Sub-17")
        self.assertEqual(self.grupo.categoria, "Juvenil")
        self.assertTrue(self.grupo.estado)
    
    def test_grupo_str(self):
        """Test representación string de grupo"""
        self.assertEqual(str(self.grupo), "Sub-17 - Juvenil")
    
    def test_grupo_rango_edades(self):
        """Test rango de edades del grupo"""
        self.assertEqual(self.grupo.rango_edad_minima, 15)
        self.assertEqual(self.grupo.rango_edad_maxima, 17)


class InscripcionModelTest(TestCase):
    """Tests para el modelo Inscripcion"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.atleta = Atleta.objects.create(
            nombre_atleta="María",
            apellido_atleta="González",
            dni="0987654321",
            fecha_nacimiento=date(2008, 3, 20),
            sexo="Femenino"
        )
        
        self.inscripcion = Inscripcion.objects.create(
            atleta=self.atleta,
            fecha_inscripcion=date.today(),
            tipo_inscripcion=TipoInscripcion.NUEVO
        )
    
    def test_inscripcion_creation(self):
        """Test creación de inscripción"""
        self.assertEqual(self.inscripcion.atleta, self.atleta)
        self.assertEqual(self.inscripcion.tipo_inscripcion, TipoInscripcion.NUEVO)
        self.assertFalse(self.inscripcion.habilitada)
    
    def test_inscripcion_habilitar(self):
        """Test habilitar inscripción"""
        self.inscripcion.habilitar()
        self.assertTrue(self.inscripcion.habilitada)
    
    def test_inscripcion_deshabilitar(self):
        """Test deshabilitar inscripción"""
        self.inscripcion.habilitar()
        self.inscripcion.deshabilitar()
        self.assertFalse(self.inscripcion.habilitada)


class PruebaAntropometricaModelTest(TestCase):
    """Tests para el modelo PruebaAntropometrica"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.atleta = Atleta.objects.create(
            nombre_atleta="Carlos",
            apellido_atleta="López",
            dni="1122334455",
            fecha_nacimiento=date(2007, 8, 10),
            sexo="Masculino"
        )
        
        self.prueba = PruebaAntropometrica.objects.create(
            atleta=self.atleta,
            estatura=175.5,
            peso=70.0,
            altura_sentado=90.0,
            envergadura=180.0
        )
    
    def test_prueba_creation(self):
        """Test creación de prueba antropométrica"""
        self.assertEqual(self.prueba.atleta, self.atleta)
        self.assertEqual(self.prueba.estatura, 175.5)
        self.assertEqual(self.prueba.peso, 70.0)
        self.assertTrue(self.prueba.estado)
    
    def test_prueba_imc_calculado(self):
        """Test cálculo automático de IMC"""
        self.assertIsNotNone(self.prueba.indice_masa_corporal)
        # IMC = peso / (estatura en metros)^2
        esperado = round(70.0 / (1.755 ** 2), 2)
        self.assertAlmostEqual(self.prueba.indice_masa_corporal, esperado, places=1)
    
    def test_prueba_indice_cornico_calculado(self):
        """Test cálculo automático de índice córnico"""
        self.assertIsNotNone(self.prueba.indice_cornico)
        # Índice córnico = (altura_sentado / estatura) * 100
        esperado = round((90.0 / 175.5) * 100, 2)
        self.assertAlmostEqual(self.prueba.indice_cornico, esperado, places=1)
    
    def test_validar_datos(self):
        """Test validación de datos"""
        self.assertTrue(self.prueba.validar_datos())


class PruebaFisicaModelTest(TestCase):
    """Tests para el modelo PruebaFisica"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.atleta = Atleta.objects.create(
            nombre_atleta="Ana",
            apellido_atleta="Martínez",
            dni="5566778899",
            fecha_nacimiento=date(2009, 11, 25),
            sexo="Femenino"
        )
        
        self.prueba = PruebaFisica.objects.create(
            atleta=self.atleta,
            tipo_prueba=TipoPrueba.VELOCIDAD,
            resultado=12.5,
            unidad_medida="segundos"
        )
    
    def test_prueba_creation(self):
        """Test creación de prueba física"""
        self.assertEqual(self.prueba.atleta, self.atleta)
        self.assertEqual(self.prueba.tipo_prueba, TipoPrueba.VELOCIDAD)
        self.assertEqual(self.prueba.resultado, 12.5)
        self.assertTrue(self.prueba.estado)
    
    def test_validar_resultado(self):
        """Test validación de resultado"""
        self.assertTrue(self.prueba.validar_resultado())
    
    def test_comparar_resultados(self):
        """Test comparación de resultados"""
        otra_prueba = PruebaFisica.objects.create(
            atleta=self.atleta,
            tipo_prueba=TipoPrueba.VELOCIDAD,
            resultado=11.8,
            unidad_medida="segundos"
        )
        
        comparacion = self.prueba.comparar_resultados(otra_prueba)
        self.assertIn("diferencia", comparacion)
        self.assertIn("porcentaje_cambio", comparacion)


class AtletaAPITest(APITestCase):
    """Tests de API para Atleta"""
    
    def setUp(self):
        """Configuración inicial para los tests de API"""
        self.client = APIClient()
        self.grupo = GrupoAtleta.objects.create(
            nombre="Sub-12",
            rango_edad_minima=10,
            rango_edad_maxima=12,
            categoria="Menores"
        )
        
        self.atleta_data = {
            "nombre_atleta": "Pedro",
            "apellido_atleta": "Ramírez",
            "dni": "9988776655",
            "fecha_nacimiento": "2013-04-12",
            "sexo": "Masculino",
            "email": "pedro@example.com",
            "telefono": "0998765432"
        }
    
    def test_crear_atleta_api(self):
        """Test crear atleta vía API"""
        url = '/api/v1/atletas/'
        response = self.client.post(url, self.atleta_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_listar_atletas_api(self):
        """Test listar atletas vía API"""
        # Crear atleta primero
        Atleta.objects.create(
            nombre_atleta="Test",
            apellido_atleta="Atleta",
            dni="1111111111",
            fecha_nacimiento=date(2012, 1, 1),
            sexo="Masculino"
        )
        
        url = '/api/v1/atletas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_obtener_atleta_api(self):
        """Test obtener atleta específico vía API"""
        atleta = Atleta.objects.create(
            nombre_atleta="Específico",
            apellido_atleta="Test",
            dni="2222222222",
            fecha_nacimiento=date(2011, 6, 15),
            sexo="Femenino"
        )
        
        url = f'/api/v1/atletas/{atleta.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GrupoAtletaAPITest(APITestCase):
    """Tests de API para GrupoAtleta"""
    
    def setUp(self):
        """Configuración inicial para los tests de API"""
        self.client = APIClient()
        self.grupo_data = {
            "nombre": "Sub-19",
            "rango_edad_minima": 17,
            "rango_edad_maxima": 19,
            "categoria": "Junior"
        }
    
    def test_crear_grupo_api(self):
        """Test crear grupo vía API"""
        url = '/api/v1/grupos/'
        response = self.client.post(url, self.grupo_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_listar_grupos_api(self):
        """Test listar grupos vía API"""
        GrupoAtleta.objects.create(
            nombre="Test",
            rango_edad_minima=8,
            rango_edad_maxima=10,
            categoria="Mini"
        )
        
        url = '/api/v1/grupos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InscripcionAPITest(APITestCase):
    """Tests de API para Inscripcion"""
    
    def setUp(self):
        """Configuración inicial para los tests de API"""
        self.client = APIClient()
        self.atleta = Atleta.objects.create(
            nombre_atleta="Inscripcion",
            apellido_atleta="Test",
            dni="3333333333",
            fecha_nacimiento=date(2010, 7, 20),
            sexo="Masculino"
        )
    
    def test_crear_inscripcion_api(self):
        """Test crear inscripción vía API"""
        url = '/api/v1/inscripciones/'
        data = {
            "atleta_id": self.atleta.id,
            "fecha_inscripcion": str(date.today()),
            "tipo_inscripcion": "NUEVO"
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_listar_inscripciones_api(self):
        """Test listar inscripciones vía API"""
        url = '/api/v1/inscripciones/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PruebaAntropometricaAPITest(APITestCase):
    """Tests de API para PruebaAntropometrica"""
    
    def setUp(self):
        """Configuración inicial para los tests de API"""
        self.client = APIClient()
        self.atleta = Atleta.objects.create(
            nombre_atleta="Antropometrica",
            apellido_atleta="Test",
            dni="4444444444",
            fecha_nacimiento=date(2009, 2, 14),
            sexo="Femenino"
        )
    
    def test_crear_prueba_api(self):
        """Test crear prueba antropométrica vía API"""
        url = '/api/v1/pruebas-antropometricas/'
        data = {
            "atleta_id": self.atleta.id,
            "estatura": 160.0,
            "peso": 55.0,
            "altura_sentado": 82.0
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_listar_pruebas_api(self):
        """Test listar pruebas antropométricas vía API"""
        url = '/api/v1/pruebas-antropometricas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PruebaFisicaAPITest(APITestCase):
    """Tests de API para PruebaFisica"""
    
    def setUp(self):
        """Configuración inicial para los tests de API"""
        self.client = APIClient()
        self.atleta = Atleta.objects.create(
            nombre_atleta="Fisica",
            apellido_atleta="Test",
            dni="5555555555",
            fecha_nacimiento=date(2008, 9, 30),
            sexo="Masculino"
        )
    
    def test_crear_prueba_api(self):
        """Test crear prueba física vía API"""
        url = '/api/v1/pruebas-fisicas/'
        data = {
            "atleta_id": self.atleta.id,
            "tipo_prueba": "VELOCIDAD",
            "resultado": 13.2,
            "unidad_medida": "segundos"
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_listar_pruebas_api(self):
        """Test listar pruebas físicas vía API"""
        url = '/api/v1/pruebas-fisicas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_obtener_tipos_prueba_api(self):
        """Test obtener tipos de prueba vía API"""
        url = '/api/v1/pruebas-fisicas/tipos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HealthCheckAPITest(APITestCase):
    """Tests para el endpoint de health check"""
    
    def test_health_check(self):
        """Test endpoint de health check"""
        url = '/health/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')


class APIRootTest(APITestCase):
    """Tests para el endpoint raíz de la API"""
    
    def test_api_root(self):
        """Test endpoint raíz de la API"""
        url = '/api/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)
