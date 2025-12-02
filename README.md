# Módulo de Basketball - Django API

## Descripción
API REST para el módulo de Basketball, implementado con Django y Django REST Framework. Este módulo gestiona atletas, grupos, inscripciones, pruebas antropométricas y pruebas físicas.

## Tecnologías
- **Python 3.11+**
- **Django 4.2+**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose**

## Arquitectura
El proyecto sigue una arquitectura MVC (Model-View-Controller) adaptada a Django:

```
basketball/
├── models.py          # Modelos (ORM Django)
├── controllers/       # Controladores de lógica de negocio
│   ├── connection.py  # Conexión a base de datos
│   ├── atleta_controller.py
│   ├── grupo_atleta_controller.py
│   ├── inscripcion_controller.py
│   ├── prueba_antropometrica_controller.py
│   ├── prueba_fisica_controller.py
│   ├── entrenador_controller.py
│   └── estudiante_vinculacion_controller.py
├── services/          # Servicios API (código de estado, mensaje, data)
│   ├── api_response.py
│   ├── atleta_service.py
│   ├── grupo_atleta_service.py
│   ├── inscripcion_service.py
│   ├── prueba_antropometrica_service.py
│   ├── prueba_fisica_service.py
│   ├── entrenador_service.py
│   └── estudiante_vinculacion_service.py
├── serializers.py     # Serializers para API
├── views.py           # Vistas (ViewSets)
├── urls.py            # URLs del módulo
├── admin.py           # Configuración del admin
└── tests.py           # Tests unitarios y de integración
```

## Modelos del Diagrama de Clases

### Entidades Principales
- **Usuario** (referencia al módulo de usuarios - otro equipo)
- **Atleta** - Gestión de atletas de basketball
- **GrupoAtleta** - Agrupación de atletas por categorías
- **Entrenador** - Gestión de entrenadores
- **EstudianteVinculacion** - Estudiantes de vinculación
- **Inscripcion** - Inscripciones de atletas
- **PruebaAntropometrica** - Pruebas de medidas corporales
- **PruebaFisica** - Pruebas de rendimiento físico

## Instalación

### Con Docker (Recomendado)

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd module_basketball
```

2. Copiar el archivo de variables de entorno:
```bash
cp .env.example .env
```

3. Construir y ejecutar los contenedores:
```bash
docker-compose up --build
```

4. La API estará disponible en: `http://localhost:8000`

### Sin Docker (Desarrollo Local)

1. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno en `.env`

4. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario (opcional):
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor:
```bash
python manage.py runserver
```

## Endpoints de la API

### Base URL: `/api/v1/`

| Recurso | Endpoint | Métodos |
|---------|----------|---------|
| Atletas | `/atletas/` | GET, POST, PUT, PATCH, DELETE |
| Grupos | `/grupos/` | GET, POST, PUT, PATCH, DELETE |
| Inscripciones | `/inscripciones/` | GET, POST, PUT, PATCH, DELETE |
| Pruebas Antropométricas | `/pruebas-antropometricas/` | GET, POST, PUT, PATCH, DELETE |
| Pruebas Físicas | `/pruebas-fisicas/` | GET, POST, PUT, PATCH, DELETE |
| Entrenadores | `/entrenadores/` | GET, POST, PUT, PATCH, DELETE |
| Estudiantes Vinculación | `/estudiantes-vinculacion/` | GET, POST, PUT, PATCH, DELETE |

### Endpoints Adicionales

- `GET /api/` - Información de la API
- `GET /health/` - Health check del servicio
- `GET /admin/` - Panel de administración Django

### Formato de Respuesta

Todas las respuestas siguen el formato:
```json
{
    "status": "success|error",
    "code": 200,
    "message": "Mensaje descriptivo",
    "data": { ... }
}
```

## Tests

Ejecutar tests:
```bash
python manage.py test basketball
```

Con coverage:
```bash
coverage run manage.py test basketball
coverage report
```

## Docker Commands

```bash
# Construir contenedores
docker-compose build

# Ejecutar contenedores
docker-compose up

# Ejecutar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener contenedores
docker-compose down

# Ejecutar migraciones en contenedor
docker-compose exec web python manage.py migrate

# Crear superusuario en contenedor
docker-compose exec web python manage.py createsuperuser
```

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| DEBUG | Modo debug | True |
| SECRET_KEY | Clave secreta Django | - |
| DB_NAME | Nombre de la base de datos | basketball_db |
| DB_USER | Usuario de PostgreSQL | postgres |
| DB_PASSWORD | Contraseña de PostgreSQL | postgres |
| DB_HOST | Host de PostgreSQL | db |
| DB_PORT | Puerto de PostgreSQL | 5432 |

## Nota sobre el Módulo de Usuario

El modelo `Usuario` está incluido como referencia para las relaciones. Cuando el módulo de usuario sea implementado por el otro equipo, se debe:

1. Remover el modelo `Usuario` de este módulo
2. Importar el modelo del módulo de usuarios
3. Actualizar las relaciones en los modelos `Entrenador` y `EstudianteVinculacion`

## Licencia

Este proyecto es parte del sistema de gestión deportiva institucional.
