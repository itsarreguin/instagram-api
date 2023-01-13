""" Authentication URL's module """

# Python standard library
from typing import List

# Django imports
from django.urls import path
from django.urls import include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Instagram views
from instagram.apps.authentication.views import AuthenticationViewSet


app_name: str = 'auth'

router = DefaultRouter()
router.register(prefix=r'auth', viewset=AuthenticationViewSet, basename='auth')

urlpatterns: List[path] = [

    path('', include(router.urls))
]