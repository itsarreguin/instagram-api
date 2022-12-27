""" User app module config """

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """ Config class """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.users'
    verbose_name: str = 'Users'