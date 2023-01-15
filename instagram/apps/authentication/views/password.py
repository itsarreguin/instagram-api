""" Authentication password views """

# Python standard library
from typing import Any

# JSON Web Token
import jwt

# Django imports
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# Instagram serializers
from instagram.apps.authentication.serializers import PasswordResetSerializer
# Instagram tasks
from instagram.apps.authentication.tasks import password_reset_email


class RequestPasswordResetAPIView(APIView):
    """
    Obtain the user email and send password reset email
    """

    def post(self, request: Request, *args: Any, **kwargs: Any):
        try:
            user = get_user_model().objects.get(email=request.data['email'])

            if user:
                password_reset_email.apply_async(args=[user.id, request.get_host()])

                return Response(
                    data = {
                        'message': 'Successful operation.',
                        'more_info': f'Password reset email sent to {user.email}. Please check your address.'
                    },
                    status = status.HTTP_200_OK
                )

        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response(
                data = { 'detail': 'User with this email not found.' },
                status = status.HTTP_404_NOT_FOUND
            )


class PasswordResetAPIView(APIView):
    """
    Verify user token an change the old password
    """

    def post(self, request: Request, token: str, *args: Any, **kwargs: Any):
        print(token)