""" Authentication views """

# Python standard library
from typing import Type

# Django REST Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework import status

# Instagram models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.accounts.serializers import UserModelSerializer
from instagram.apps.authentication.serializers import (
    SignUpSerializer,
    AccountVerificationSerializer,
    LoginSerializer
)
# Instagram tasks
from instagram.apps.accounts.tasks import send_verification_email


class AuthenticationViewSet(mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """User auth viewset

    Viewset that controls user authentication
    """

    queryset = User.objects.all()

    def get_permissions(self) -> Type[BasePermission]:
        """ Add permissions depends on the action """
        permissions = []

        if self.action in ['signup', 'verification', 'login']:
            permissions = [AllowAny]

        return [permission() for permission in permissions]

    def get_serializer_class(self) -> Type[Serializer | ModelSerializer]:
        """ Returns a serializer class depends on the action """
        if self.action == 'signup':
            return SignUpSerializer

        if self.action == 'verification':
            return AccountVerificationSerializer

        if self.action == 'login':
            return LoginSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request: Request) -> Type[Response]:
        """ Users signup action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            send_verification_email.apply_async(args=[user.id], countdown=5)

            return Response(
                data = {
                    'message': 'Account has been created successfully',
                    'data': UserModelSerializer(instance=user).data
                },
                status = status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verification(self, request: Request) -> Type[Response]:
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data={ 'message': 'Your account has been verified.' },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request: Request) -> Type[Response]:
        """ Users login action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user, token = serializer.save()

            data = {
                'user': UserModelSerializer(instance=user).data,
                'access_token': token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)