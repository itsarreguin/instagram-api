""" Core app config """

from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    """ Config class """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instagram.core'
    verbose_name = 'Core'