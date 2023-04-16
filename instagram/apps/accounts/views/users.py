""" Main user views module """

# Python standard library
from typing import Any
from typing import Type

# Django imports
from django.db.models import QuerySet

# Django REST Framework
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework import status

# Instagram models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.accounts.serializers import (
    UserModelSerializer,
    UserSerializer
)
# Instagram permissions
from instagram.apps.accounts.permissions import IsAccountOwner


class UserViewSet(viewsets.ModelViewSet):
    """ User viewset class

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """

    lookup_field = 'username'

    def get_permissions(self) -> Type[BasePermission]:
        """ Add permissions for user actions """
        permissions = [IsAuthenticated]

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permissions.append(IsAccountOwner)

        return [permission() for permission in permissions]

    def get_queryset(self, *args: tuple[any], **kwargs: dict[str, Any]) -> QuerySet:
        """ Returns queryset type if username is present """
        if kwargs:
            return User.objects.filter(*args, **kwargs).first()

        return User.objects.all()

    def get_serializer_class(self) -> Type[Serializer | ModelSerializer]:
        """ Return serializers depends on the action """
        if self.action in ['retrieve', 'destroy']:
            return UserModelSerializer
        if self.action in ['update', 'partial_update']:
            return UserSerializer

    def retrieve(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        serializer_class = self.get_serializer_class()
        queryset = self.get_queryset(username=kwargs['username'])

        serializer = serializer_class(instance=queryset)

        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            data = { 'detail': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def update(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        serializer_class = self.get_serializer_class()
        queryset = self.get_queryset(username=kwargs['username'])

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

    def partial_update(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        # TODO: Implementation soon
        pass

    def destroy(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        queryset = self.get_queryset(username=kwargs['username'])

        if queryset:
            queryset.update(is_active=False)

            return Response(
                data = { 'message': 'User has been deleted' },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )