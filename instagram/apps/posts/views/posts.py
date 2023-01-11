""" Views module for Posts app """

# Python standard library
from typing import Any

# Django REST Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Instagram Serializers
from instagram.apps.posts.serializers import (
    PostCreateSerializer,
    PostModelSerializer,
    PostDetailSerializer,
)
# Instagram permissions
from instagram.apps.posts.permissions import IsPostOwner


class PostViewSet(viewsets.ModelViewSet):
    """ Post view set class

    This view controls all actions linked on the posts
    """

    lookup_field = 'url'

    def get_queryset(self, url: str = None):
        if url is None:
            return self.get_serializer().Meta.model.objects.all()

        return self.get_serializer().Meta.model.objects.filter(url=url).first()

    def get_serializer_class(self):
        """ Return serializer based on action """
        if self.action == 'create':
            return PostCreateSerializer
        if self.action in ['list', 'retrieve']:
            return PostDetailSerializer
        if self.action in ['update', 'partial_update', 'destroy']:
            return PostModelSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]

        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsPostOwner)

        return [permission() for permission in permissions]

    def list(self, request: Request, url = None, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data, context={ 'request': request })

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, url = None, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset(url=url)
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(instance=queryset, context={ 'request': request })

        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def update(self, request: Request, url = None, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset(url=url)
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(instance=queryset, data=request.data)

        if queryset:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request: Request, url = None, *args: Any, **kwargs: Any) -> Response:
        post = self.get_queryset(url=url)

        if post:
            post.delete()

            return Response(
                data = { 'message': 'Post deleted successfully' },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )