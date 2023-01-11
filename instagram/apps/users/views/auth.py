""" Authentication views for users app """

# Django REST Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status

# Instagram models
from instagram.apps.users.models import User
# Instagram serializers
from instagram.apps.users.serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)


class UserAuthViewSet(mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """User auth viewset

    Viewset that controls user authentication
    """

    queryset = User.objects.all()

    def get_permissions(self):
        """ Add permissions depends on the action """
        permissions = []

        if self.action in ['signup', 'verification', 'login']:
            permissions = [AllowAny]

        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """ Returns a serializer class depends on the action """
        if self.action == 'signup':
            return UserSignUpSerializer

        if self.action == 'verification':
            return AccountVerificationSerializer

        if self.action == 'login':
            return UserLoginSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request: Request):
        """ Users signup action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = UserModelSerializer(instance=user).data

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verification(self, request: Request):
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
    def login(self, request: Request):
        """ Users login action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user, token = serializer.save()

            data = {
                'user': UserModelSerializer(instance=user).data,
                'access_token': token
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)