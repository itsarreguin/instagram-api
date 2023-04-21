""" User app permission classes """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """ Provides account access to user owner """

    def has_object_permission(self, request, view, obj) -> bool:
        """ Verify if the object and user are the same """
        return bool(request.user == obj)

    def has_permission(self, request, view):
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)