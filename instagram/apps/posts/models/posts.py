""" Posts models module """

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models import User


class Post(models.Model):
    """Post model class

    Fields:
        author (foreign key): One to many relationship
        image (image field): Contains post image
        url (slugf ield): Storage random string to use as url
        description (text field): Image post description
    """
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_('image'),
        blank=False,
        null=False,
        upload_to='users/posts'
    )
    url = models.SlugField(_('url'), unique=True, blank=True)
    description = models.TextField(_('description '), blank=True)

    class Meta:
        """ Meta class options """
        verbose_name: str = _('Post')
        verbose_name_plural: str = _('Posts')

    def __str__(self) -> str:
        return 'Post by @%s' % self.author.username