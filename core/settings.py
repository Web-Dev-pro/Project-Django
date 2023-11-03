import dj_database_url
import os
from datetime import timedelta
from pathlib import Path

import environ
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# MVV, CBV, FBV
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production! I know
DEBUG = True

# Application definition
ALLOWED_HOSTS = ["ontahsil.uz", "35.178.137.119", "api.ontahsil.uz", 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://ontahsil.uz', 'https://ontahsil.uz', 'http://35.178.137.119', "https://api.ontahsil.uz", "https://ontahsil.uz"]

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'drf_yasg',
    'corsheaders',
    'phonenumber_field',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'debug_toolbar',
    'schema_graph',
    'channels',
    'django_celery_beat',
    'django_celery_results',

    # local apps
    'apps.initialization.apps.InitializationConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.comment.apps.CommentConfig',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# write a database example for postgresql
# setup postgresql database
# DATABASES = {
#     'default': {
#         'ENGINE': env('ENGINE'),
#         'NAME': env('NAMEDB'),
#         'USER': env('USERDB'),
#         'PASSWORD': env("PASSWORD"),
#         'HOST': env('HOST'),
#         'PORT': env('PTDB'),
#     }
# }
# for test
# DATABASES = {
#     'default': {
#         'ENGINE': env('ENGINE'),
#         'NAME': env('DB_SEC_NAME'),
#         'USER': env('DB_SEC_USER'),
#         'PASSWORD': env("DB_SEC_PASS"),
#         'HOST': env('DB_SEC_URL'),
#         'PORT': env('PTDB'),
#     }
# }

# Celery configuration
# CELERY_BROKER_URL = env("BROKER_URL")
# CELERY_RESULT_BACKEND = env("BROKER_URL")

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_WORKER_CONCURRENCY = 1
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [('localhost', 6379)],
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'EXCEPTION_HANDLER': 'apps.initialization.views.custom_exception_handler',
}
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
REST_AUTH = {
    'SESSION_LOGIN': True,
    "USE_JWT": True,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# configure cors hozircha True holatida bo'ladi keyinchalik alohida whitelist beriladi CORS uchun
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# SETUP CACHES
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         "LOCATION": "redis://default:BvdF6ukWOSEOSWV7xw8LfXADD8B1O9Cu@redis-18763.c277.us-east-1-3.ec2.cloud.redislabs.com:18763",
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'TIMEOUT': 600,
#     }
# }


# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

# for email verification
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMALI_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'husanboy0250@gmail.com'
# EMAIL_HOST_PASSWORD = "Onajonim1234@"
# EMAIL_USE_TLS = True


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# hozircha uchun
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            'format': '{levelname} {asctime} [{module}:{lineno}] {message}',
            "style": "{",
        },
    },
    'handlers': {
        'error_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './error.log',
            'formatter': 'verbose',
        },
        'info_log': {
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': './info.log',
            'formatter': 'verbose',
        },
        'debug_log': {
            'level': "DEBUG",
            'class': "logging.FileHandler",
            'filename': './debug.log',
            'formatter': 'verbose',
        },
        'warning_log': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': './warning.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['error_log', 'info_log', 'debug_log', 'warning_log'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
