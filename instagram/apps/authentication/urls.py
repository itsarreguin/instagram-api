""" Authentication URL's module """

# Python standard library
from typing import List

# Django imports
from django.urls import path, re_path
from django.urls import include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Instagram views
from instagram.apps.authentication.views import AuthenticationViewSet
from instagram.apps.authentication.views.password import (
    RequestPasswordResetAPIView,
    PasswordResetAPIView,
)


app_name: str = 'auth'

router = DefaultRouter()
router.register(prefix=r'auth', viewset=AuthenticationViewSet, basename='auth')

urlpatterns: List[path] = [

    path(
        route = '',
        view = include(router.urls)
    ),
    path(
        route = 'auth/password/reset/',
        view = RequestPasswordResetAPIView.as_view(),
        name = 'request-password-reset'
    ),
    re_path(
        route = r'auth/password/reset/(?P<token>[a-zA-Z0-9\._-]+)/',
        view = PasswordResetAPIView.as_view(),
        name = 'reset-password'
    )
]