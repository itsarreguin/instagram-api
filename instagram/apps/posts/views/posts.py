""" Views module for Posts app """

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.serializers import PostModelSerializer


class PostViewSet(viewsets.ModelViewSet):
    """"""
    serializer_class = PostModelSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self, url: str = None):
        if url is None:
            return self.get_serializer().Meta.model.objects.all()

        return self.get_serializer().Meta.model.objects.filter(url=url).first()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)