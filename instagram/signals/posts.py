from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save
)
from django.utils.crypto import get_random_string

from instagram.apps.posts.models import Post


@receiver(post_save, sender=Post)
def post_save_generate_url(sender, instance, created, *args, **kwargs):
    if not instance.url:
        instance.url = get_random_string(length=32)
        instance.save()