from rest_framework import generics
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied, ValidationError

from base import serializers
from base import models
from base import permissions
from base import libs


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']










class CreateUserAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.User.objects.all()
    serializer_class   = serializers.UserSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("User Created Successfully")
        return response

Create_User = CreateUserAPI.as_view()








class UpdateUserAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.User.objects.all()
    serializer_class   = serializers.UserSerializer
    role_access_list   = ['owner', 'admin', 'manager', 'reception', 'waiter']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("User Updated successfully")
        return response
    
Update_User = UpdateUserAPI.as_view()




class GetUserAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.User.objects.all()
    serializer_class   = serializers.UserSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj

Get_User = GetUserAPI.as_view()







class ListUserAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.User.objects.all()
    serializer_class   = serializers.UserSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['username', 'phone_number']

    def get_queryset(self):
        user          = self.request.user
        lower_roles   = libs.get_lower_roles(user)   
        branches      = libs.get_branch_ids(self)
        if branches == ['all']:
            branches = models.Branch.objects.all()
        query = models.User.objects.filter(role__in = lower_roles, branch__in = branches)
        return query
    
List_User = ListUserAPI.as_view()






