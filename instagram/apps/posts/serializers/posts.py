""" Serializers module for Posts """

# Django REST Framework
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
    likes = serializers.SerializerMethodField('get_total_likes', read_only=True)
    comments = serializers.SerializerMethodField('get_total_comments', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'image',
            'url',
            'description',
            'author',
            'likes',
            'comments',
            'created',
            'modified'
        ]

        read_only_fields = fields

    def get_author(self, obj) -> dict[str, str]:
        return {
            'username': obj.author.username,
            'full_name': obj.author.profile.full_name,
        }

    def get_total_likes(self, obj) -> int:
        return obj.likes.count()

    def get_total_comments(self, obj) -> int:
        return obj.comments.count()