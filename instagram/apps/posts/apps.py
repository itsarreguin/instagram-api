""" Post app configuration module """

from django.apps import AppConfig


class PostsConfig(AppConfig):
    """ Post config class """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instagram.apps.posts'
    verbose_name: str = 'Post'