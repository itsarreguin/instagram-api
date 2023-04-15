""" Notifications app module """

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    """ Notifications app config class """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.notifications'
    verbose_name: str = _('Notifications')