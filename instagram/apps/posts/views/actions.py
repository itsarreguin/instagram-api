# Python standard library
from typing import Any

# Django Framework
from django.db.models import QuerySet
from django.db.models import Model

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.models import Like
from instagram.apps.posts.models import Comment
from instagram.apps.notifications.models import NoificationType
# Instagram serializers
from instagram.apps.posts.serializers import CommentDetailSerializer
# Instagram tasks
from instagram.apps.notifications.tasks import send_notification


class ActionsMixin(APIView):

    def get_queryset(self, klass: Model, *args: tuple[Any], **kwargs: dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return klass.objects.filter(*args, **kwargs)

        return klass.objects.all()


class LikeAPIView(ActionsMixin):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        if post:
            like = Like.objects.create(user=request.user, post=post)
            if post.author != like.user:
                send_notification.apply_async(kwargs={
                    'sender_username': self.request.user.username,
                    'receiver_username': like.user.username,
                    'category': NoificationType.LIKE,
                    'object_id': like.id
                })
            return Response(
                data={
                    'message': f'Like added to @{post.author.username} post'
                },
                status=status.HTTP_201_CREATED
            )

        return Response({ 'info': 'Post not found' }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        like = self.get_queryset(Like, id=kwargs['id'])

        if post and like:
            like.delete()
            return Response(
                data={ 'message': f'Like removed from {post.author.username} post' },
                status=status.HTTP_200_OK
            )

        return Response({ 'info': 'Post not found' }, status=status.HTTP_404_NOT_FOUND)


class CommentAPIView(ActionsMixin):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, **kwargs: dict[str, Any]) -> Response:
        serializer_class = CommentDetailSerializer
        if id in kwargs:
            post = self.get_queryset(Post, url=kwargs['url']).first()
            comment = self.get_queryset(Comment, post=post).first()
            serializer = serializer_class(instance=comment)

            return Response(serializer.data, status=status.HTTP_200_OK)

        post = self.get_queryset(Post, url=kwargs['url']).first()
        comments = self.get_queryset(Comment, post=post)
        serializer = serializer_class(comments, many=True)

        return Response({ 'message': 'Comments list', 'comments': serializer.data })

    def post(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        data = request.data
        post = self.get_queryset(Post, url=kwargs['url']).first()
        if post:
            comment = Comment.objects.create(author=request.user, post=post, body=data['body'])
            if comment.author != post.author:
                send_notification.apply_async(kwargs={
                    'sender_username': self.request.user.username,
                    'receiver_username': comment.author.username,
                    'category': NoificationType.COMMENT,
                    'object_id': comment.id
                })
            return Response(
                data={ 'message': f'Comment added to @{post.author.username} post' },
                status=status.HTTP_201_CREATED
            )

        return Response(
            data={ 'info': 'Post not found' },
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        comment = self.get_queryset(Comment, id=kwargs['id'])
        if post and comment:
            comment.delete()

            return Response(
                data={ 'message': f'Comment removed from @{post.author.username} post' },
                status=status.HTTP_200_OK
            )

        return Response(
            data={ 'info': 'Post or comment not found' },
            status=status.HTTP_404_NOT_FOUND
        )