""" Production settings file """

from instagram.settings.base import *


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS')


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

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# Cache framework
# https://docs.djangoproject.com/en/4.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_CACHE_URL'),
    }
}


# Email configuration
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# CORS
CORS_ALLOWED_ORIGINS = []