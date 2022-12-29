""" Users URL's and routing module """

from typing import List

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from instagram.apps.users.views import UserViewSet


app_name: str = 'users'

router = DefaultRouter()
router.register(prefix=r'users', viewset=UserViewSet, basename='users')

urlpatterns: List[path] = [

    path(route='', view=include(router.urls))
]