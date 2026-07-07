import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in {'1', 'true', 'yes', 'on'}
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',') if os.environ.get('DJANGO_ALLOWED_HOSTS') else ['*']


def get_database_config():
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:IYfovFwyiuEHkFjnQCfziuArEnGGSusV@postgres.railway.internal:5432/railway')
    if database_url:
        parsed = urlparse(database_url)
        if parsed.scheme == 'sqlite':
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': str(BASE_DIR / parsed.path.lstrip('/')),
            }

        options = {}
        if parsed.hostname and ('neon.tech' in parsed.hostname or 'railway.internal' in parsed.hostname):
            options['sslmode'] = 'require'
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or 'postgres',
            'PASSWORD': parsed.password or 'IYfovFwyiuEHkFjnQCfziuArEnGGSusV',
            'HOST': parsed.hostname or 'postgres.railway.internal',
            'PORT': str(parsed.port or 5432),
            'OPTIONS': options,
        }

    sqlite_path = BASE_DIR / 'db.sqlite3'
    if sqlite_path.exists():
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(sqlite_path),
        }

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'stocknet'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'stocknet_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stocknet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stocknet.wsgi.application'
DATABASES = {'default': get_database_config()}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny']}
