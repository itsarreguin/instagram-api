""" Authentication password views """

# Python standard library
from typing import Any

# JSON Web Token
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    PyJWTError
)

# Django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
    """ Request Password Reset API View class

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
    """ Password Reset API View class

    Verify user token an change the old or forgot password.
    """

    def post(self, request: Request, token: str, *args: Any, **kwargs: Any):
        serializer = PasswordResetSerializer(data=request.data)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.filter(username=payload['user']).first()

        except ExpiredSignatureError:
            raise ValidationError('Password reset link has been expired')
        except PyJWTError:
            raise ValidationError('Invalid token')

        if payload['type'] != 'password_reset':
            raise ValidationError('Invalid token type')

        if serializer.is_valid(raise_exception=True) and user:
            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response(
                data = { 'message': 'Password reset successfully' },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'detail': 'User not found or expired token' },
            status = status.HTTP_400_BAD_REQUEST
        )