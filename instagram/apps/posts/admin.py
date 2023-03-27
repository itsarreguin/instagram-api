# Django imports
from django.contrib import admin

# instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.models import Comment
from instagram.apps.posts.models import Like


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):

    list_display = [
        'author',
        'url',
        'description'
    ]

    list_display_links = [
        'author',
        'url',
        'description',
    ]


@admin.register(Comment)
class CommentAdminModel(admin.ModelAdmin):

    list_display = [
        'id',
        'author',
        'body'
    ]

    list_display_links = ['id', 'author']


@admin.register(Like)
class LikeAdminModel(admin.ModelAdmin):

    list_display = ['id', 'user']
    list_display_links = ['id', 'user']