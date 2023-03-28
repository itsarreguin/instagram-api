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
from instagram.apps.posts.views import CommentAPIView


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
    path(
        route='posts/<str:url>/comments/',
        view=CommentAPIView.as_view(),
        name='comment'
    ),
    path(
        route='posts/<str:url>/comments/<int:id>/',
        view=CommentAPIView.as_view(),
        name='comment-destroy'
    )
]