from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']






class CreateSchoolAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("School Created successfully")
        return response
Create_School = CreateSchoolAPI.as_view()






class UpdateSchoolAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("School Updated successfully")
        return response
Update_School = UpdateSchoolAPI.as_view()




class GetSchoolAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_School = GetSchoolAPI.as_view()







class ListSchoolAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'address'] 
List_School = ListSchoolAPI.as_view()






