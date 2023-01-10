""" Signals for posts app """

# Django imports
from django.dispatch import receiver
from django.db.models.signals import post_save

# Instagram models
from instagram.core.models import User
from instagram.apps.users.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def save_full_name(sender, instance, created, *args, **kwargs):
    if not instance.full_name:
        first_name = instance.user.first_name
        last_name = instance.user.last_name

        instance.full_name = first_name + ' ' + last_name

        instance.save()