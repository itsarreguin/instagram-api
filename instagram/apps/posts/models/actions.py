""" Models that represents an action in a post """

# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models.abstracts import BaseAbstractModel
from instagram.apps.posts.models.posts import Post


class Comment(BaseAbstractModel):

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(_('body'), max_length=455, blank=True, null=True)
    url = models.CharField(_('url'), max_length=155, unique=True, blank=False, null=False)

    class Meta:
        verbose_name: str = _('Comment')
        verbose_name_plural: str = _('Comments')

    def __str__(self) -> str:
        return 'by @%s' % self.author.username


class Like(BaseAbstractModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        verbose_name: str = _('Like')
        verbose_name_plural: str = _('Likes')

    def __str__(self) -> str:
        return 'by @%s' % self.user.username