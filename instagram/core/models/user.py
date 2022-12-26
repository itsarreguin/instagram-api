""" Custom user classes """

from typing import (
    Any,
    Optional
)

from django.contrib.auth.models import UserManager as BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ):
        if not username:
            raise ValueError('Username is required field')
        elif not email:
            raise ValueError('Email address is required field')

        email = self.normalize_email(email=email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)

        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        return user

    def create_user(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_verified', False)

        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=40, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True)

    username_regex_validator = RegexValidator(
        regex=r'^([\w\d\._]+[^\s\-@\*\[\{(\)\}\]\/\+:,;\\%&$]){4,30}$',
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
        regex=r'^([a-zA-Z0-9\._-]{4,}[^\s])@\w{2,8}\.\w{2,15}(\.\w{2,15})?$'
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

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'email']

    class Meta:
        """ Meta class """
        verbose_name: str = _('User')
        verbose_name_plural: str = _('Users')

    def __str__(self) -> str:
        return self.get_username

    @property
    def get_username(self) -> str:
        return '%s' % self.username

    def get_full_name(self) -> str:
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self) -> str:
        return '%s' % self.first_name