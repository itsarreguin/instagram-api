""" Abstract models """

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseAbstractModel(models.Model):
    """ Base abstract model class

    This is an abstract model only for models inheritance
    """

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        """ Meta class options """
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']