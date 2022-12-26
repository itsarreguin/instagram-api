""" Development settings file """

from instagram.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-j-rb2bfx2&ex^n7as2jhutrcfa6psshs3a1ae!e$)0dkvffx0w')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1'
]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Channel layers
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Cache framework
# https://docs.djangoproject.com/en/4.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


# Email configuration
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER_DEV')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_DEV')


# CORS
CORS_ALLOWED_ORIGINS = []


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'