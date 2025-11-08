# PythonAnywhere uchun settings.py o'zgarishlar

# 1. DEBUG = False (Production uchun)
DEBUG = False

# 2. ALLOWED_HOSTS sozlash
ALLOWED_HOSTS = [
    'yourusername.pythonanywhere.com',  # Sizning PythonAnywhere domain
    '127.0.0.1',
    'localhost',
]

# 3. Database - SQLite production uchun
import os
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 4. Static files sozlash
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 5. Security sozlamalari
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 6. CORS (agar kerak bo'lsa)
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
]

# 7. Logging (Production uchun)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}