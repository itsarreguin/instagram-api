""" Celery application config """

# Python imports
import os

# Celery imports
from celery import Celery

# Django imports
from django.apps import apps
from django.conf import settings


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram.settings.dev')


celery = Celery('instagram')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object(obj='django.conf:settings', namespace='CELERY')

celery.autodiscover_tasks()