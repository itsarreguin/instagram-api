""" Views module for Posts app """

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.serializers import PostModelSerializer


class PostViewSet(viewsets.ModelViewSet):
    """"""
    serializer_class = PostModelSerializer