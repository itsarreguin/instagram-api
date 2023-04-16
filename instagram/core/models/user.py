""" Custom user classes """

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Instagram managers
from instagram.core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=40, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True)

    username_regex_validator = RegexValidator(
        regex=r'^([\w\d\._]+[^\s\-@\*\[\{(\)\}\]\/\+:,;\\%&$]){3,30}$',
        message='Username can be only contains letters, numbers, . or _'
    )

    username = models.CharField(
        verbose_name=_('username'),
        unique=True,
        max_length=30,
        blank=False,
        null=False,
        validators=[username_regex_validator]
    )

    email_regex_validator = RegexValidator(
        regex=r'^([a-zA-Z0-9\._-]{3,}[^\s])@\w{2,25}\.\w{2,15}(\.\w{2,15})?$'
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
        max_length=255,
        blank=False,
        null=False,
        validators=[email_regex_validator]
    )

    is_active = models.BooleanField(_('is active'), default=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_verified = models.BooleanField(_('is verified'), default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        """ Meta class """
        verbose_name: str = _('User')
        verbose_name_plural: str = _('Users')

    def __str__(self) -> str:
        return '%s' % self.username

    def get_full_name(self) -> str:
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self) -> str:
        return '%s' % self.first_name

    @property
    def total_posts(self) -> int:
        return self.posts.count()

    @property
    def total_notifications(self) -> int:
        return self.notifications.count()

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    @property
    def total_comments(self) -> int:
        return self.comments.count()