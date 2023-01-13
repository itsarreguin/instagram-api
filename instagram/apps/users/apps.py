""" User app module config """

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """ User config class """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.users'
    verbose_name: str = _('Users')

    def ready(self) -> None:
        from instagram.signals import profile