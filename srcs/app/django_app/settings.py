from pathlib import Path
from decouple import config
import logging

# Configuration of the logger
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('transcendence')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-c_dug2-$h$y^4#6c1sj2qh9@%x7wq7vd#_@=5e-7blbl%7!3sz'

DEBUG = True

# The host for the front end 
# (Need to be changed in production, need to be the IP or the domain name of the front end)
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
	'daphne',
	'transcendence',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware for the API Django
# Middleware : A framework of hooks into Django’s request/response processing.
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


# ASGI application for websocket and asyncronous tasks

ASGI_APPLICATION = 'django_app.asgi.application'

CHANNEL_LAYERS = {
	'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Connexion database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Authentication with Django

AUTH_USER_MODEL = 'transcendence.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentification 42
API_42_UID = config('CLIENT_ID')
API_42_SECRET = config('CLIENT_SECRET')
API_42_REDIRECT_URI = 'https://localhost:8000/api/login42/'

# Internationalization

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

# FRONT END AND MEDIA
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
STATIC_ROOT = '/var/www/static/'

# For the API and the front end URL
ROOT_URLCONF = 'django_app.urls'

# The Template HTML for the front end
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# CORS AND CSRF
CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = [
#     "https://localhost:8000",
# 	"https://api.intra.42.fr"
# ]

CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'content-type',
    'origin',
    'x-csrftoken',
    'x-requested-with',
    'accept',
    'authorization',
    'x-csrftoken'
]
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [
#     "https://localhost:8000",
# 	"https://api.intra.42.fr"
# ]

# Utiliser le header HTTP X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Définir SECURE_PROXY_SSL_HEADER si vous utilisez un proxy inverse comme Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Rediriger les requêtes HTTP vers HTTPS
SECURE_SSL_REDIRECT = False

# Utiliser des cookies sécurisés
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configuration HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True