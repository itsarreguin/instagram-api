""" Main user views module """

# Python standard library
from typing import Any

# Django REST Framework
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Instagram models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.users.serializers import (
    UserModelSerializer,
    UserSerializer
)
# Instagram permissions
from instagram.apps.users.permissions import IsAccountOwner


class UserViewSet(viewsets.ModelViewSet):
    """ User viewset class

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """

    lookup_field = 'username'

    def get_permissions(self):
        """ Add permissions for user actions """
        permissions = [IsAuthenticated]

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permissions.append(IsAccountOwner)

        return [permission() for permission in permissions]

    def get_queryset(self, username: str = None):
        """ Returns queryset type if username is present """
        if not username:
            return User.objects.all()

        return User.objects.filter(username=username).first()

    def get_serializer_class(self):
        """ Return serializers depends on the action """
        if self.action in ['retrieve', 'destroy']:
            return UserModelSerializer
        if self.action in ['update', 'partial_update']:
            return UserSerializer

    def retrieve(self, request: Request, username: str, *args: Any, **kwargs: Any) -> Response:
        serializer_class = self.get_serializer_class()
        queryset = self.get_queryset(username=username)

        serializer = serializer_class(instance=queryset)

        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            data = { 'detail': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def update(self, request: Request, username: str, *args: Any, **kwargs: Any) -> Response:
        serializer_class = self.get_serializer_class()
        queryset = self.get_queryset(username=username)

        serializer = serializer_class(instance=queryset, data=request.data)

        if queryset and serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                data = {
                    'message': 'User has been updated successfully',
                    'data': serializer.data
                },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def partial_update(self, request: Request, username: str, *args: Any, **kwargs: Any) -> Response:
        # TODO: Implementation soon
        pass

    def destroy(self, request: Request, username: str, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset(username=username)

        if queryset:
            User.objects.filter(username=username).update(is_active=False)

            return Response(
                data = { 'message': 'User has been deleted' },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )