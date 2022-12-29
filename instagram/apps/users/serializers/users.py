""" Users serializers """

from django.contrib.auth import (
    password_validation,
    authenticate
)
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from instagram.apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer class

    Fields:
        serializers (_type_): _description_
    """

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer class

    Fields:
        first_name (charfield): Get and validate user first name
        last_name (charfield): Get and validate user last_name
        username (charfield): Validate and register new username
        email (emailfield): Validate if email address is unique
        password (charfield): Validate and hashing user password
        password_confirmation (charfield): Only to confirm that the password is correct
    """

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    username_regex_validator = RegexValidator(
        regex=r'^([\w\d\._]+[^\s\-@\*\[\{(\)\}\]\/\+:,;\\%&$]){2,30}$',
        message='Username can be only contains letters, numbers, . or _'
    )
    username = serializers.CharField(
        min_length=2,
        max_length=30,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            username_regex_validator,
        ]
    )

    email_regex_validator = RegexValidator(
        regex=r'^([a-zA-Z0-9\._-]{3,}[^\s])@\w{2,25}\.\w{2,15}(\.\w{2,15})?$'
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            email_regex_validator
        ]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        password = data['password']
        password_conf = data['password_confirmation']

        if password != password_conf:
            raise serializers.ValidationError('Password didn\'t match')

        password_validation.validate_password(password)

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')

        user = User.objects.create_user(**validated_data, is_verified=False)

        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer class

    Fields:
        username (charfield): _description_
        password (charfield): _description_
    """