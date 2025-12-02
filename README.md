# Módulo Basketball - Plantilla para Trabajo en Grupo

## Estructura del Proyecto

```
basketball_template/
├── basketball/                    # App principal
│   ├── controllers/               # Controladores (por implementar)
│   ├── dao/                       # Data Access Objects (implementado)
│   ├── services/                  # Servicios de negocio (por implementar)
│   ├── management/commands/       # Comandos personalizados (por implementar)
│   ├── migrations/                # Migraciones de la base de datos
│   ├── models.py                  # Modelos (por implementar)
│   ├── serializers.py             # Serializadores (por implementar)
│   ├── urls.py                    # URLs (por implementar)
│   └── views.py                   # Vistas (por implementar)
├── basketball_project/            # Configuración del proyecto Django
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # URLs del proyecto
│   ├── wsgi.py                    # WSGI
│   └── asgi.py                    # ASGI
├── media/                         # Archivos multimedia
├── staticfiles/                   # Archivos estáticos
├── requirements.txt               # Dependencias
└── .env.example                   # Variables de entorno ejemplo
```

## Configuración Inicial

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. Ejecutar migraciones:
```bash
python manage.py migrate
```

5. Iniciar servidor:
```bash
python manage.py runserver
```

## Asignación de Tareas por Equipo

### Modelos (models.py)
- [ ] Usuario
- [ ] Atleta
- [ ] GrupoAtleta
- [ ] Inscripcion
- [ ] PruebaAntropometrica
- [ ] PruebaFisica
- [ ] Entrenador
- [ ] EstudianteVinculacion

### Serializadores (serializers.py)
- [ ] UsuarioSerializer
- [ ] AtletaSerializer
- [ ] GrupoAtletaSerializer
- [ ] InscripcionSerializer
- [ ] PruebaAntropometricaSerializer
- [ ] PruebaFisicaSerializer
- [ ] EntrenadorSerializer
- [ ] EstudianteVinculacionSerializer

### Services
- [ ] atleta_service.py
- [ ] entrenador_service.py
- [ ] estudiante_vinculacion_service.py
- [ ] grupo_atleta_service.py
- [ ] inscripcion_service.py
- [ ] prueba_antropometrica_service.py
- [ ] prueba_fisica_service.py

### Controllers
- [ ] atleta_controller.py
- [ ] entrenador_controller.py
- [ ] estudiante_vinculacion_controller.py
- [ ] grupo_atleta_controller.py
- [ ] inscripcion_controller.py
- [ ] prueba_antropometrica_controller.py
- [ ] prueba_fisica_controller.py

### URLs y Views
- [ ] urls.py
- [ ] views.py

## DAO (Ya Implementado)

El patrón DAO (Data Access Object) ya está implementado en `basketball/dao/`:
- `generic_dao.py`: DAO genérico con operaciones CRUD
- `model_daos.py`: DAOs específicos para cada modelo

### Uso del DAO

```python
from basketball.dao import AtletaDAO

# Instanciar DAO
atleta_dao = AtletaDAO()

# Operaciones CRUD
atleta = atleta_dao.create(nombre_atleta="Juan", ...)
atletas = atleta_dao.find_all()
atleta = atleta_dao.find_by_id(1)
atleta_dao.update(1, nombre_atleta="Pedro")
atleta_dao.delete(1)
```
