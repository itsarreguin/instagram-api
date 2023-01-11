""" User serializer classes """

# Django REST framework
from rest_framework import serializers

# Instagram models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.users.serializers.profile import ProfileModelSerializer


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