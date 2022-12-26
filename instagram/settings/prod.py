""" Production settings file """

from instagram.settings.base import *


SECRET_KEY = env('SECRET_KEY', cast=str)

DEBUG = env('DEBUG', cast=bool)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {},
    'instagram': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'instagram_service',
            'passfile': '.postgres_pass'
        }
    }
}


# Channel layers
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# Cache framework
# https://docs.djangoproject.com/en/4.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.str('REDIS_CACHE_URL'),
    }
}


# Email configuration
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

EMAIL_BACKEND = env('EMAIL_BACKEND', cast=str)
EMAIL_HOST = env('EMAIL_HOST', cast=str)
EMAIL_PORT = env('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', cast=str)


# CORS
CORS_ALLOWED_ORIGINS = []


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'