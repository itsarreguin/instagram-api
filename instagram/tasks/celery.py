""" Celery tasks app config """

# Python imports
import os

# Celery imports
from celery import Celery

# Django imports
from django.apps import AppConfig
from django.apps import apps
from django.conf import settings
from django.utils.translation import gettext_lazy as _


if not settings.configured:
    # Set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings.dev')


celery = Celery('instagram')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object(obj='django.conf:settings', namespace='CELERY')


class CeleryAppConfig(AppConfig):
    """ Config class """
    name: str = 'instagram.tasks'
    verbose_name: str = _('Celery')

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        # Load task modules from all registered Django app configs.
        celery.autodiscover_tasks(lambda: installed_apps, force=True)