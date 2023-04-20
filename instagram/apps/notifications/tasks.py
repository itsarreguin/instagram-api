# Python standard library
from typing import Type

# Django helpers
from django.contrib.auth import get_user_model

# Instagram celery
from instagram import celery
# Instagram models
from instagram.core.models import User
from instagram.apps.notifications.models import Notification


@celery.task
def send_notification(
    sender_username: str = None,
    receiver_username: str = None,
    category: str = None,
    object_id: int = None
) -> None:
    try:
        sender = get_user_model().objects.filter(username=sender_username).first()
        receiver = get_user_model().objects.filter(username=receiver_username).first()
        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            category=category,
            object_id=object_id
        )
    except get_user_model().DoesNotExist:
        pass