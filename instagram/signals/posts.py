""" Signals for posts application """

# Python standard library
from typing import Any

# Django imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.db.models import Model

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.models import Comment
# Instagram utils
from instagram.utils import RAND_CHARS


@receiver(post_save, sender=Post)
def generate_url(sender: Model, instance: Post, **kwargs: Any):
    """generate_url

    Signal that generates a random string to be saved as url for a post.

    Args:
        sender (Model): The model that sends the signal
        instance (Post model): Instance of the same model that send a signal
    """

    if not instance.url:
        instance.url = get_random_string(length=32, allowed_chars=RAND_CHARS)
        instance.save()


@receiver(post_save, sender=Comment)
def comment_url(sender: Model, instance: Comment, **kwargs) -> None:
    """ Save comment url """
    if not instance.url:
        instance.url = get_random_string(length=32, allowed_chars=RAND_CHARS)
        instance.save()