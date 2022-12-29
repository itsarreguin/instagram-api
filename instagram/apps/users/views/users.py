""" Users views module """

from rest_framework import viewsets
from rest_framework.decorators import action


class UserViewSet():
    """User viewset

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """