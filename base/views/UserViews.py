from rest_framework import generics
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from rest_framework.request import Request
from django.http import HttpRequest, QueryDict
from rest_framework.test import APIRequestFactory, force_authenticate
import json

from base import serializers
from base import models
from base import permissions
from base import views
from base import libs


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']










class CreateUserAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.User.objects.all()
    serializer_class   = serializers.UserSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data       = request.data.copy()   
            staff_data = {
                key.replace('staff_', ''): data.pop(key) for key in list(data.keys()) if key.startswith('staff_')
            }
            request._full_data       = data 
            response                 = super().create(request, *args, **kwargs)        #create user instance
            
            if staff_data['images']:
                staff_data['images']    = list(staff_data['images']) if not isinstance(staff_data['images'], list) else staff_data['images']                
            staff_data['phone_number']  = self.instance.phone_number
            staff_data['branch']        = self.instance.branch.id
            staff_data['is_user']       = True
            staff_request               = self._clone_request(request, staff_data)
            staff_response              = views.Create_Staff(staff_request)
            if staff_response.status_code != 201:
                raise ValidationError(staff_response.data)

            self.instance.staff      = models.Staff.objects.get(id = staff_response.data["id"])
            self.instance.save()
            response.data            = serializers.UserSerializer(self.instance).data
            response.data['message'] = _("User Created successfully")
            return response
        
    def perform_create(self, serializer):
        self.instance = serializer.save()

    def _clone_request(self, original_request, new_data):
        """Helper function to create a modified Django HttpRequest with files support"""
        factory = APIRequestFactory()
        django_request = factory.post(
            path=original_request.path,
            data=new_data,
            format='multipart' if original_request.FILES else 'json'
        )

        # Copy user and authentication data
        django_request.user = original_request.user
        django_request.auth = original_request.auth

        # Handle file uploads
        django_request.FILES.update(original_request.FILES)

        return django_request

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






