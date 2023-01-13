""" Users URL's and routing module """

# Python standard library
from typing import List

# Django imports
from django.urls import path, include

# Django REST Fraework imports
from rest_framework.routers import DefaultRouter

# Instagram views
from instagram.apps.users.views import UserViewSet
from instagram.apps.users.views import UserAuthViewSet


app_name: str = 'users'

router = DefaultRouter()
router.register(prefix=r'auth', viewset=UserAuthViewSet, basename='auth')
router.register(prefix=r'users', viewset=UserViewSet, basename='users')

urlpatterns: List[path] = [

    path(route='', view=include(router.urls))
]