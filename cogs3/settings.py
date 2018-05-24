"""
Django settings for cogs3 project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url

from django.contrib.messages import constants as messages
from dotenv import load_dotenv

from selenium import webdriver

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# load environment variables from .env
dotenv_file = os.path.join(BASE_DIR, 'cogs3', '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'institution.apps.InstitutionConfig',
    'project.apps.ProjectConfig',
    'system.apps.SystemConfig',
    'users.apps.UsersConfig',
    'dashboard.apps.DashboardConfig',
    'widget_tweaks',
    'shibboleth',
    'cookielaw',
    'django_rq',
    'security',
    'openldap',
    'notification',
    'hreflang',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.SCWRemoteUserMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'shibboleth.backends.ShibbolethRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'cogs3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Use project level template directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shibboleth.context_processors.login_link',
                'shibboleth.context_processors.logout_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'cogs3.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=500,
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-gb'
LOCALE_PATHS = ('locale', )
TEMPLATE_CONTEXT_PROCESSORS = ('django.template.context_processors.i18n', )

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Email
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

# Shibboleth
SHIBBOLETH_IDENTITY_PROVIDER_LOGIN = os.environ.get('SHIBBOLETH_IDENTITY_PROVIDER_LOGIN')
SHIBBOLETH_IDENTITY_PROVIDER_LOGOUT = os.environ.get('SHIBBOLETH_IDENTITY_PROVIDER_LOGOUT')
SHIBBOLETH_ATTRIBUTE_MAP = {
    'REMOTE_USER': (True, 'username'),
}
SHIBBOLETH_FORCE_REAUTH_SESSION_KEY = 'shib_force_reauth'
# Shibboleth users must apply for an account
CREATE_UNKNOWN_USER = False

# Redis Queue
RQ_SHOW_ADMIN_LINK = True
RQ_QUEUES = {
    'default': {
        'HOST': os.environ.get('RQ_HOST'),
        'PORT': os.environ.get('RQ_PORT'),
        'DB': os.environ.get('RQ_DB'),
        'PASSWORD': os.environ.get('RQ_PASSWORD'),
        'DEFAULT_TIMEOUT': os.environ.get('RQ_DEFAULT_TIMEOUT'),
    }
}

# OpenLDAP
OPENLDAP_HOST = os.environ.get('OPENLDAP_HOST')
OPENLDAP_JWT_KEY = os.environ.get('OPENLDAP_JWT_KEY')
OPENLDAP_JWT_ISSUER = os.environ.get('OPENLDAP_JWT_ISSUER')
OPENLDAP_JWT_AUDIENCE = os.environ.get('OPENLDAP_JWT_AUDIENCE')
OPENLDAP_JWT_ALGORITHM = os.environ.get('OPENLDAP_JWT_ALGORITHM')

# Logging
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'general': {
            'format':
            '[%(asctime)s] %(levelname)s [%(name)s - %(filename)s:%(lineno)s] %(message)s '
            '(EXCEPTION: %(exc_info)s)',
            'datefmt':
            '%d/%b/%Y %H:%M:%S'
        },
        'request': {
            'format':
            '[%(asctime)s] %(levelname)s [%(name)s - %(filename)s:%(lineno)s] %(message)s '
            '(STATUS: %(status_code)s; REQUEST: %(request)s; EXCEPTION: %(exc_info)s)',
            'datefmt':
            '%d/%b/%Y %H:%M:%S'
        },
        'db': {
            'format':
            '[%(asctime)s] %(levelname)s [%(name)s - %(filename)s:%(lineno)s] %(message)s '
            '(DURATION: %(duration)s; SQL: %(sql)s; PARAMS: %(params)s; EXCEPTION: %(exc_info)s)',
            'datefmt':
            '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'general',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'django': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'general',
        },
        'security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'security.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'general',
        },
        'db': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'db.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'db',
        },
        'request': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'request.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'request',
        },
        'queue': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'queue.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'general',
        },
        'apps': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'apps.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'general',
        },
        'openldap': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'openldap.log'),
            'maxBytes': 16 * 1024 * 1024,  # 16 MB
            'backupCount': 5,
            'formatter': 'general',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['request', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'queue': {
            'handlers': ['queue'],
            'level': 'WARNING',
        },
        'apps': {
            'handlers': ['apps'],
            'level': 'WARNING',
        },
        'common': {
            'handlers': ['apps'],
            'level': 'WARNING',
        },
        'openldap': {
            'handlers': ['openldap', 'mail_admins'],
            'level': 'WARNING',
        },
        'py.warnings': {
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

SELENIUM_WEBDRIVER = webdriver.Firefox
