# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.apps.notifications.views import NotificationsAPIView


app_name: str = 'notifications'

urlpatterns: List[path] = [
    path('notifications/', NotificationsAPIView.as_view(), name='all')
]