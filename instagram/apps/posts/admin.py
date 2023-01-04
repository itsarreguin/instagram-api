from django.contrib import admin

from instagram.apps.posts.models import Post


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):

    list_display = [
        'author',
        'url',
        'description'
    ]