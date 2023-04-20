# Python standard library
from typing import List
from typing import Type

# Django imports
from django.db.models import Model

# Django REST Framework
from rest_framework import serializers

# Instagram models
from instagram.apps.notifications.models import Notification


class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model: Type[Model] = Notification
        fields: List[str] = [
            'sender',
            'category',
            'is_read',
            'created',
        ]