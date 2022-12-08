import os

from corsheaders.defaults import default_headers, default_methods
from smart_getenv import getenv
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/0.1.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'ilova_backend_4.1.0_0.1.0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG', type=bool, default=True)

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', type=list, default=[])

# If the app is running behind a proxy, this variable must be set with the proxy path
# See https://docs.djangoproject.com/en/0.1.0/ref/settings/#force-script-name



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'corsheaders',
    'django_extensions',
    'django_filters',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'phonenumber_field',
    'sendsms',

    # Local apps
    'apps.accounts.apps.AccountsConfig',
    'apps.suggestions.apps.SuggestionsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.application_info',
            ]
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/0.1.0/ref/settings/#databases

DATABASES_ENGINE_MAP = {
    'mysql': 'django.db.backends.mysql',
    'oracle': 'django.db.backends.oracle',
    'postgresql': 'django.db.backends.postgresql',
    'postgresql_psycopg2': 'django.db.backends.postgresql_pycopg2',
    'sqlite3': 'django.db.backends.sqlite3',
}

DATABASES = {
    'default': {
        'ENGINE': DATABASES_ENGINE_MAP.get(os.getenv('DB_ENGINE', 'sqlite3')),
        'NAME': os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'CONN_MAX_AGE': getenv('DB_CONN_MAX_AGE', type=int, default=0),
    }
}

if os.environ.get('DB_ENGINE') == 'oracle':
    DATABASES['default']['OPTIONS'] = {'threaded': True, 'use_returning_into': False}

# Password validation
# https://docs.djangoproject.com/en/0.1.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/0.1.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/0.1.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]


# django-cors-headers
# https://pypi.org/project/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = getenv('CORS_ORIGIN_ALLOW_ALL', type=bool, default=True)
CORS_ORIGIN_WHITELIST = getenv('CORS_ORIGIN_WHITELIST', type=list, default=[])
CORS_ORIGIN_REGEX_WHITELIST = [
    '%r' % value
    for value in getenv('CORS_ORIGIN_REGEX_WHITELIST', type=list, default=[])
]
CORS_ALLOW_HEADERS = getenv(
    'CORS_ALLOW_HEADERS', type=list, default=list(default_headers)
)
CORS_ALLOW_METHODS = getenv(
    'CORS_ALLOW_METHODS', type=list, default=list(default_methods)
)

# Django REST framework
# http://www.django-rest-framework.org/api-guide/settings/


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}
AUTH_USER_MODEL = 'accounts.PhoneNumberAbstactUser'
# AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = (
    'apps.accounts.backends.phone_backend.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=3000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Phone number field
PHONENUMBER_DEFAULT_REGION = 'UZ'

# Token length for OTP
TOKEN_LENGTH = 6

# Token expiry
TOKEN_EXPIRE_MINUTES = 1

# Application definitions

APP_VERSION = '1.0.0'
APP_NAME = 'Ilova API'
APP_DESCRIPTION = 'A RESTfull API for project Ilova API'


# Sms sending confs
PHONE_LOGIN_ATTEMPTS = 10
PHONE_LOGIN_OTP_LENGTH = 6
PHONE_LOGIN_OTP_HASH_ALGORITHM = 'sha256'
PHONE_LOGIN_DEBUG = True

# Configure the ESKIZ (for eskiz_sms integration)
ESKIZ_EMAIL = os.getenv('ESKIZ_EMAIL')
ESKIZ_PASSWORD = os.getenv('ESKIZ_PASSWORD')
