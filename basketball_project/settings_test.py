"""
Configuración de settings para tests usando SQLite
"""

from basketball_project.settings import *

# Override database to use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Use simpler email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
