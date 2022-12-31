from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save
)

# Instagram models
from instagram.core.models import User
from instagram.apps.users.models import Profile


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_create(sender, instance, *args, **kwargs):
    pass


@receiver(post_save, sender=Profile)
def post_save_full_name(sender, instance, created, *args, **kwargs):
    if not instance.full_name:
        first_name = instance.user.first_name
        last_name = instance.user.last_name

        instance.full_name = first_name + ' ' + last_name

        instance.save()