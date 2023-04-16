""" Accounts app module config """

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    """ User config class """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.accounts'
    verbose_name: str = _('Accounts')

    def ready(self) -> None:
        from instagram.signals import profile