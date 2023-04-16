# Django imports
from django.contrib import admin

# Instagram models
from instagram.apps.accounts.models import Profile


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'is_public'
    ]

    actions = ['change_public_status']

    def change_public_status(self, request, queryset):
        if request.user.profile.is_public:
            queryset.update(is_public=False)
        else:
            queryset.update(is_public=True)

    change_public_status.short_description = 'Change public status'