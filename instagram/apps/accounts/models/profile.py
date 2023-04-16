""" Profile model classes """

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Instgram models
from instagram.core.models.abstracts import BaseAbstractModel
from instagram.core.models import User


class Profile(BaseAbstractModel):
    """ User profile model """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    full_name = models.CharField(_('full name'), max_length=150, blank=False, null=False)
    picture = models.ImageField(
        verbose_name=_('picture picture'),
        blank=True,
        null=True,
        upload_to='users/profile'
    )
    biography = models.TextField(_('biography'), blank=True)
    link = models.URLField(_('website'), blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True)

    class Meta:
        """ Meta class """
        verbose_name: str = _('Profile')
        verbose_name_plural: str = _('Profiles')

    def __str__(self) -> str:
        return '@%s' % self.user.username