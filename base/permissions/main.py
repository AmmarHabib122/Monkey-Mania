from rest_framework.permissions import BasePermission
from base import models
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _



class Authenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            raise PermissionDenied(_("User is not logged in"))
        return True
    


            
class RoleAccess(BasePermission):
    def has_permission(self, request, view):
        role_access_list = getattr(view, "role_access_list", [])
        if request.user.role not in role_access_list:
            raise PermissionDenied(_("You Do not have the permission to perform this action"))
        return True

    