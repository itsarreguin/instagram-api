""" Users URL's and routing module """

# Python standard library
from typing import List

# Django imports
from django.urls import path, include

# Django REST Fraework imports
from rest_framework.routers import DefaultRouter

# Instagram views
from instagram.apps.accounts.views import UserViewSet


app_name: str = 'accounts'

router = DefaultRouter()
router.register(prefix=r'accounts', viewset=UserViewSet, basename='users')

urlpatterns: List[path] = [

    path(route='', view=include(router.urls))
]