""" Views module for Posts app """

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.serializers import (
    PostModelSerializer,
    PostDetailSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """"""
    serializer_class = PostModelSerializer
    lookup_field = 'url'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self, url: str = None):
        if url is None:
            return self.get_serializer().Meta.model.objects.all()

        return self.get_serializer().Meta.model.objects.filter(url=url).first()

    def list(self, request, url = None, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, url = None, *args, **kwargs):
        queryset = self.get_queryset(url=url)
        serializer = PostDetailSerializer(instance=queryset, context = {'request': request})

        if queryset:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, url = None, *args, **kwargs):
        post = self.get_queryset(url=url)

        if post:
            post.delete()

            return Response(
                data = { 'message': 'Post deleted successfully' },
                status = status.HTTP_200_OK
            )

        return Response(
            data = { 'error': 'Resource not found' },
            status = status.HTTP_404_NOT_FOUND
        )