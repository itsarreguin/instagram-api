""" Serializers for posts actions """

# Django REST Framework
from rest_framework import serializers

# Instagram models
from instagram.apps.posts.models import Comment


class CommentDetailSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField('get_author', read_only=True)

    class Meta:
        model = Comment

        fields= [
            'id',
            'author',
            'body',
            'created'
        ]

        read_only_fileds = fields

    def get_author(self, obj) -> dict[str, str]:
        return {
            'username': obj.author.username,
            'full_name': obj.author.profile.full_name
        }