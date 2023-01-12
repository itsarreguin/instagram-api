""" Authentication user serializers """

import jwt

# Django imports
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Instagram models
from instagram.core.models import User


class SignUpSerializer(serializers.Serializer):
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
        user = User.objects.create_user(**validated_data)

        return user


class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer class

    Fields:
        token (charfield): Check user token to verify their account
    """

    token = serializers.CharField()

    def validate_token(self, data):
        """ Verify if user token is valid """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has been expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'verification_email':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload

        return data

    def save(self):
        """ Change user verification status to True """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True

        user.save()



class LoginSerializer(serializers.Serializer):
    """User login serializer class

    Fields:
        username (charfield): Check if username exists
        password (charfield): Check if user password is correct
    """

    username = serializers.CharField(min_length=3, max_length=30)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account has not been verified yet')

        self.context['user'] = user

        return data

    def create(self, data):
        """ Generate or get user token """
        token, created = Token.objects.get_or_create(user=self.context['user'])

        return self.context['user'], token.key