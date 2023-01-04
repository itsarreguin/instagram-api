""" Posts app URL's module """

from typing import List

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from instagram.apps.posts.views import PostViewSet


router = DefaultRouter()
router.register(prefix=r'posts', viewset=PostViewSet, basename='posts')

urlpatterns: List[path] = [
    path('', view=include(router.urls))
]