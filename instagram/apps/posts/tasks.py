""" Background tasks for Posts app """

from PIL import Image

from instagram.tasks import celery


@celery.task
def resize_post_imeg():
    pass