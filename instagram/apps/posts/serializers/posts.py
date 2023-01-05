""" Serializers module for Posts """

from rest_framework import serializers

# Instagram models
from instagram.apps.posts.models import Post
# Instagram serializers
from instagram.apps.users.serializers import UserModelSerializer


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

        exclude = [
            'author',
            'url',
            'created',
            'modified'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        Post.objects.create(author=user, **validated_data)

        return validated_data


class PostModelSerializer(serializers.ModelSerializer):

    author = UserModelSerializer(source='user', read_only=True)

    class Meta:
        model = Post

        fields = [
            'author',
            'description',
            'url'
        ]


class PostDetailSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField(read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name = 'posts:posts-detail',
        lookup_field = 'url',
        read_only = True
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'image',
            'url',
            'author',
            'description',
            'created',
            'modified'
        ]

        extra_kwargs = {
            'image': { 'read_only': True },
            'description': { 'read_only': True },
        }

    def get_author(self, obj):
        return {
            'username': obj.author.username,
            'full_name': obj.author.profile.full_name,
            'date_joined': obj.author.date_joined
        }