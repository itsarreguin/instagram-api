""" Serializers module for Posts """

from rest_framework import serializers

# Instagram models
from instagram.apps.posts.models import Post
# Instagram serializers
from instagram.apps.users.serializers import UserModelSerializer


class PostModelSerializer(serializers.ModelSerializer):

    author = UserModelSerializer(source='user', read_only=True)

    class Meta:
        model = Post

        fields = [
            'author',
            'description'
            'url'
        ]

        extra_kwargs = {}