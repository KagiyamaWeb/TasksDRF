from rest_framework import permissions
from User.models import Role, User
from django.contrib.auth.models import Group, AnonymousUser


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the admin role (role ID 2)
        if type(request.user) != AnonymousUser:
            return request.user.roles.filter(id=2).exists()
        return False