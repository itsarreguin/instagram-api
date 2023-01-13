""" Background tasks for Posts app """

# Celery import
from celery import shared_task

# Pillow imports
from PIL import Image

# Instagram tasks
from instagram.tasks import celery


@celery.task
def resize_post_image():
    pass