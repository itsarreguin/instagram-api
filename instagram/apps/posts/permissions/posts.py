""" Posts app permission classes """

from rest_framework.permissions import BasePermission


class IsPostOwner(BasePermission):
    """ Provides access for posts actions """

    def has_object_permission(self, request, view, obj):
        """ Check if the user is the posts author """
        return request.user == obj.author