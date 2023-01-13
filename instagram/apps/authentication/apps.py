""" Authentication app module """

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    """ Authentication app config class"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instagram.apps.authentication'
    verbose_name = _('Auth')