""" Posts app permission classes """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsPostAuthor(BasePermission):
    """ Provides access for posts actions """

    def has_object_permission(self, request, view, obj) -> bool:
        """ Check if the user is the posts author """
        return bool(request.user == obj.author)

    def has_permission(self, request, view) -> bool:
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)