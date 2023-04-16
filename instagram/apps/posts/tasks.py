""" Background tasks for Posts app """

# Celery import
from instagram import celery

# Pillow imports
from PIL import Image


@celery.task
def resize_post_image():
    pass