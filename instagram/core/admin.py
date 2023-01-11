""" Admin user model actions and definitions """

# Django imports
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

# Instagram models
from instagram.core.models import User


class CustomUserAdmin(UserAdmin):
    """ Admin user model """

    list_display = [
        'username',
        'first_name',
        'last_name',
        'is_verified',
        'is_active'
    ]

    list_display_links = ['username', 'first_name',]

    list_filter = [
        'username',
        'first_name',
        'last_name',
        'is_verified'
    ]

    actions = [
        'enable_user',
        'verified_account',
        'disable_user',
        'unverified_account',
    ]

    def enable_user(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_active=True)

    enable_user.short_description = 'Enable user'

    def verified_account(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_verified=True)

    verified_account.short_description = 'Verify account'

    def disable_user(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_active=False)

    disable_user.short_description = 'Disable user'

    def unverified_account(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_verified=False)

    unverified_account.short_description = 'Unverify account'


admin.site.register(User, CustomUserAdmin)