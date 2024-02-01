"""
Django settings for gemusaba project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import sentry_sdk
from decouple import config, Csv
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="awesome_secret_key_here")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='')


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'drf_yasg',
    'users',
    'apps',
    'apis'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# For silence the warning from django-admin-interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

ROOT_URLCONF = 'gemusaba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'gemusaba.wsgi.application'

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if config('DATABASE_DEVELOPMENT', default=True, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': f"django.db.backends.{config('DATABASE_TYPE', default='postgresql')}",
            'NAME': config(
                'DATABASE_NAME',
                default='gemusaba-database'),
            'USER': config(
                'DATABASE_USER',
                default='gemusaba'),
            'PASSWORD': config(
                'DATABASE_PASSWORD',
                default='gemusaba'),
            'HOST': config(
                'DATABASE_HOST',
                default='localhost'),
            'PORT': config(
                'DATABASE_PORT',
                default=''),
        }}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django crispy forms and template configuration

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# More Django settings
# https://docs.djangoproject.com/en/5.0/ref/settings/

CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool, default=False)

SESSION_COOKIE_AGE = 86400  # Set the session cookie age to only 1 day (in seconds)

# Logging
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGS_FILE = 'logs/gemusaba.log'
LOGS_FILE_MAX_SIZE = 1024 * 1024 * 10  # 10 MB
LOGS_FILE_MAX_BACKUPS = 20


# Check if logs directory exists, if not create it
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create log file if doesn't exist
if not os.path.exists(LOGS_FILE):
    open(LOGS_FILE, 'w').close()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] {%(name)s:%(lineno)s} [%(levelname)s] - %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S %z',
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'production_log_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_FILE,
            'formatter': 'standard',
            # Clean log after server restart if DEBUG is True
            'mode': 'w' if DEBUG else 'a',
        },
        'debug_log_file': {
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_FILE,
            'maxBytes': LOGS_FILE_MAX_SIZE,
            'backupCount': LOGS_FILE_MAX_BACKUPS,
            'formatter': 'standard',
            # Clean log after server restart if DEBUG is True
            'mode': 'w' if DEBUG else 'a'
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'debug_log_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': True
        } if DEBUG else {
            'handlers': ['console', 'production_log_file'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': True
        },
        "django": {
            "handlers": ["console", "mail_admins", 'debug_log_file'],
            "level": "INFO",
        } if DEBUG else {
            "handlers": ["console", "mail_admins", 'production_log_file'],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server", 'debug_log_file'],
            "level": "INFO",
            "propagate": False,
        } if DEBUG else {
            "handlers": ["django.server", 'production_log_file'],
            "level": "INFO",
            "propagate": False,
        }
    }
}

# Django email backend configuration
# https://docs.djangoproject.com/en/4.2/topics/email

ENABLE_EMAIL = config('ENABLE_EMAIL', cast=bool, default=False)

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=25)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=False)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)

if ENABLE_EMAIL:
    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / "emails"

# Sentry Integration
# https://docs.sentry.io/platforms/python/integrations/django/

if config('ENABLE_SENTRY', cast=bool, default=False):
    sentry_sdk.init(
        dsn=config('SENTRY_DSN', default=''),
        enable_tracing=True,
        # Send PII data to Sentry
        send_default_pii=True,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=config('SENTRY_TRACES_SAMPLE_RATE', cast=float, default=1.0),
        # TODO: Versioning when production version plan is ready
        integrations=[
            DjangoIntegration(
                # make Sentry use URL path as transaction name instead of view function name
                transaction_style='url',
                # Track middleware performance
                middleware_spans=True,
                # Track Django signal performance (for example of signal, see signals.py in users app)
                # This will be used more in the future like sending email when on event, etc.
                signals_spans=True,
                # See how many cache hits/misses there are
                cache_spans=False
            )
        ]
    )
