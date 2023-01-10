""" User permission classes """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """ Provides account access to user owner """

    def has_object_permission(self, request, view, obj):
        """ Verify if the object and user are the same """
        return request.user == obj