""" User profile serializers """

# Django REST Framework
from rest_framework import serializers

# Instagram models
from instagram.apps.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """ Serializer user profile data """

    class Meta:
        """ Meta class """
        model = Profile
        fields = [
            'full_name',
            'picture',
            'biography',
            'link'
        ]