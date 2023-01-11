""" Signals for posts app """

# Python standard library
from typing import Any

# Django imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Model

# Instagram models
from instagram.core.models import User
from instagram.apps.users.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender: Model, instance: User, created: User, **kwargs: Any):
    """ create user profile

    Save a profile after than new user has been created
    """

    if created:
        profile = Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def save_full_name(sender: Model, instance: Profile, **kwargs: Any):
    """ save full_name

    Save the full name that will be displayed on the profile, taking the first and last name using
    the user model relationship.
    """

    if not instance.full_name:
        first_name = instance.user.first_name
        last_name = instance.user.last_name

        instance.full_name = first_name + ' ' + last_name

        instance.save()