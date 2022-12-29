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
)


class UserViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    """User viewset

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'signup':
            permissions = [AllowAny]

        return [permission() for permission in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """ Users signup action """
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            data = UserModelSerializer(instance=user).data

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)