""" Posts app URL's module """

# Python standard library
from typing import List

# Django imports
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Instagram views
from instagram.apps.posts.views import PostViewSet
from instagram.apps.posts.views import LikeAPIView


app_name: str = 'posts'

router = DefaultRouter()
router.register(prefix=r'posts', viewset=PostViewSet, basename='posts')

urlpatterns: List[path] = [

    path('', view=include(router.urls)),
    path(
        route='posts/<str:url>/likes/',
        view=LikeAPIView.as_view(),
        name='like'
    ),
    path(
        route='posts/<str:url>/likes/<int:id>/',
        view=LikeAPIView.as_view(),
        name='unlike'
    ),
]