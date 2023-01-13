""" Post app configuration module """

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    """ Post config class """

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.apps.posts'
    verbose_name: str = _('Posts')

    def ready(self) -> None:
        from instagram.signals import posts