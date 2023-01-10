from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

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

    actions = ['change_verification_status']

    def change_verification_status(self, request, queryset):
        if request.user.is_verified:
            queryset.update(is_verified=False)
        else:
            queryset.update(is_verified=True)

    change_verification_status.short_description = 'Change verification status'


admin.site.register(User, CustomUserAdmin)