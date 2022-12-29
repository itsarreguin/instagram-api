""" Users views module """

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Instagram Models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.users.serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)


class UserViewSet(mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """User viewset

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """
    queryset = User.objects.filter(is_active=True, is_verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup', 'verification', 'login']:
            permissions = [AllowAny]

        return [permission() for permission in permissions]

    def get_serializer_class(self):
        return super().get_serializer_class()

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """ Users signup action """
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            data = UserModelSerializer(instance=user).data

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verification(self, request):
        serializer = AccountVerificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data={ 'message': 'Your account has been verified.' },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """ Users login action """
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user, token = serializer.save()

            data = {
                'user': UserModelSerializer(instance=user).data,
                'access_token': token
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)