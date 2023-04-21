# Python standard library
from typing import Any
from typing import Dict
from typing import Type

# Django imports
from django.db.models import QuerySet

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework import status

# Instagram models
from instagram.core.models import User
from instagram.apps.notifications.models import Notification
from instagram.apps.notifications.models import NoificationType
# Instagram serializers
from instagram.apps.notifications.serializers import NotificationsSerializer


class NotificationsAPIView(ListAPIView):

    serializer_class: Type[BaseSerializer] = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return self.get_serializer().Meta.model.objects.filter(*args, **kwargs)

        return self.get_serializer().Meta.model.objects.all()

    def list(self, request: Request, **kwargs: Dict[str, Any]) -> Response:
        queryset = self.get_queryset(receiver=self.request.user).all()
        if len(queryset) == 0:
            return Response(
                data={ 'message': 'There are no notifications' },
                status=status.HTTP_200_OK
            )
        serializer = self.serializer_class(instance=queryset, many=True)

        return Response(
            data={ 'notifications': serializer.data },
            status=status.HTTP_200_OK
        )