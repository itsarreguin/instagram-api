""" User serializer classes """

# PYthon standard library
from typing import Any

# Django REST framework
from rest_framework import serializers

# Instagram models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.accounts.serializers.profile import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer class

    Fields:
        username (charfield): Username from user
        first_name (charfield): User first name
        last_name (charfield): User last name
        email (emailfield): Get the user email address
    """

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'profile'
        ]


class UserSerializer(serializers.ModelSerializer):
    """User serializer class

    Fields:
        username (charfield): Get and check new username
        email (emailfield): Verify if email address is unique
        password (charfield): Get an validate the password
    """

    class Meta:
        """ Meta class """
        model = User

        fields = [
            'username',
            'email',
            'password'
        ]

    def validate_username(self, data: Any):
        username = User.objects.filter(username=data).exists()

        if username:
            raise serializers.ValidationError('This username is taken')

        return data

    def validate_email(self, data: Any):
        email = User.objects.filter(email=data).exists()

        if email:
            raise serializers.ValidationError(
                detail='An account with this email address already exist'
            )

        return data

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()

        return updated_user