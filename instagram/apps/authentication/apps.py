""" Authentication app module """

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    """ Authentication app config class"""

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.authentication'
    verbose_name: str = _('Auth')