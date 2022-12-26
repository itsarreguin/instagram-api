from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Models
from instagram.core.models import User


class CustomUserAdmin(UserAdmin):
    """ Admin user model """

    list_display = [
        'username',
        'first_name',
        'last_name',
        'username',
        'is_verified'
    ]

    list_display_links = [
        'username',
        'first_name',
    ]

    list_filter = [
        'username',
        'first_name',
        'last_name',
        'is_verified'
    ]

admin.site.register(User, CustomUserAdmin)