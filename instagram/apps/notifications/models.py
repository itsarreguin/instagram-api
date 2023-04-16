# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models.abstracts import BaseAbstractModel


class NoificationType(models.TextChoices):

    LIKE = 'like', _('Post liked')
    COMMENT = 'comment', _('Post commented')


class Notification(BaseAbstractModel):

    receiver = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='receiver'
    )
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sender'
    )
    category = models.CharField(
        verbose_name=_('category'),
        max_length=100, choices=NoificationType.choices
    )
    object_slug = models.CharField(_('object slug'), max_length=255, null=True)

    class Meta:
        verbose_name: str = _('Notification')
        verbose_name_plural: str = _('Notifications')

    def __str__(self) -> str:
        return 'Notification: from %s to %s' % (
            self.sender.username,
            self.receiver.username,
        )