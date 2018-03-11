"""
Django settings for openfruit project.

Generated by 'django-admin startproject' using Django 1.8.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import datetime
from django.contrib import messages
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u#@o=t712pxpr*tgsx+cx7u!wj2l#4j-1!+t+v5e%g#(+y+7v!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

ALLOWED_HOSTS = ['*',]
LOCAL_HOST = os.environ.get('LOCAL_HOST')
if LOCAL_HOST:
        ALLOWED_HOSTS.append(LOCAL_HOST)



# Application definition

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'bootstrap3',
    'datetimewidget',
    'auditlog',
    'sorl.thumbnail',
    'crispy_forms',
    'colorful',
    'corsheaders',
    'django_geo_db',
    'openfruit',
    'openfruit.common',
    'openfruit.taxonomy',
    'openfruit.reports.event',
    'openfruit.reports.review',
    'openfruit.reports.work',
    'openfruit.userdata',
    'openfruit.chat',
    'openfruit.dashboard',
    'openfruit.geography',
    'openfruit.fruit_reference',
    'openfruit.fruit_search',
    'openfruit.reports.disease',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'openfruit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'OPTIONS': {
            'loaders': ['django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader'],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django_geo_db.context_processors.google_maps_api_key',
                'django_geo_db.context_processors.google_maps_settings',
                'openfruit.userdata.context_processors.user_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'openfruit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

default = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {}
DATABASES['default'] = dj_database_url.config(default=default)
dbUsername = os.environ.get('OPENFRUIT_DB_USERNAME', '')
dbPassword = os.environ.get('OPENFRUIT_DB_PASSWORD', '')
dbHost = os.environ.get('OPENFRUIT_DB_HOST', '')

if dbHost:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'USER': dbUsername,
        'PASSWORD': dbPassword,
        'PORT': '3306',
        'HOST': dbHost,
        'NAME': 'openfruit'
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True


############
# LOGGGING #
############


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/



LOGIN_URL = '/api-auth/login/'
LOGIN_REDIRECT_URL = '/'

###########
#  Django Admin Bootstrap Settings

MESSAGE_TAGS = {
            messages.SUCCESS: 'alert-success success',
            messages.WARNING: 'alert-warning warning',
            messages.ERROR: 'alert-danger error'
}

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'



##########
# Group & User Model Permissions
##########
def get_user_models_for_permissions():
    from openfruit.reports.event.models import EventReport
    from openfruit.reports.review.models import FruitReview
    from openfruit.taxonomy.models import Cultivar, Species
    from django_geo_db.models import GeoCoordinate, Location

    return (
        EventReport, FruitReview,
        FruitReview, Cultivar, Species, GeoCoordinate, Location
    )

def get_curator_models():
    from openfruit.reports.event.models import EventReport
    from openfruit.reports.review.models import FruitReview
    from openfruit.taxonomy.models import Cultivar, Kingdom, Species, Genus
    from django_geo_db.models import City, Continent, Country, GeoCoordinate, Location, State

    return (
        EventReport, FruitReview,
        FruitReview, Cultivar, Kingdom,
        Species, Genus, City, Continent, Country,
        GeoCoordinate, Location, State
    )

CRISPY_TEMPLATE_PACK = 'bootstrap3'

#################
# Uploaded Images
#################
SMALL_THUMBNAILS = (125, 125)
MEDIUM_THUMBNAILS = (200, 200)
LARGE_THUMBNAILS = (300, 300)



#############
# Geography
#############
from django_geo_db.settings import GoogleMapsSettings
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
GM_SETTINGS = GoogleMapsSettings(lat=33.16025, lon=-87.6104341, zoom=4)
DEFAULT_MAP_CENTER = (39.77476, -97.11914)


################
# REST FRAMEWORK
################
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'openfruit.common.serializers.StandardResultsSetPagination',
    'PAGE_SIZE': 20
}
JWT_ALLOW_REFRESH = True
JWT_EXPIRATION_DELTA = datetime.timedelta(hours=1)

OF_API_USERNAME = os.environ.get('OF_API_USERNAME', '')
OF_API_PASSWORD = os.environ.get('OF_API_PASSWORD', '')



############
# MISC
############
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_PRELOAD_METADATA = os.environ.get('AWS_PRELOAD_METADATA', '')
AWS_QUERYSTRING_AUTH = os.environ.get('AWS_QUERYSTRING_AUTH', '')
AWS_S3_SECURE_URLS = os.environ.get('AWS_S3_SECURE_URLS', '')
AWS_S3_ENCRYPTION = os.environ.get('AWS_S3_ENCRYPTION', '')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', '')
STATICFILES_LOCATION = os.environ.get('STATICFILES_LOCATION', '')
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'whitenoise.storage.CompressedManifestStaticFilesStorage')
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
MEDIAFILES_LOCATION = os.environ.get('MEDIAFILES_LOCATION', '')
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '')
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', '')
URL_FILEBROWSER_MEDIA = os.environ.get('URL_FILEBROWSER_MEDIA', '')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

############
# Local Settings
############
try:
    from openfruit.local_settings import *
    pass
except:
    pass
