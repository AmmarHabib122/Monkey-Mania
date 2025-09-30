from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin']






class CreateBranchAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Branch.objects.all()
    serializer_class   = serializers.BranchSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Branch Created successfully")
        return response
    
    
Create_Branch = CreateBranchAPI.as_view()






class UpdateBranchAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Branch.objects.all()
    serializer_class   = serializers.BranchSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Branch Updated successfully")
        return response
Update_Branch = UpdateBranchAPI.as_view()




class GetBranchAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Branch.objects.all()
    serializer_class   = serializers.BranchSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_Branch = GetBranchAPI.as_view()







class ListBranchAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Branch.objects.all().order_by('-id')
    pagination_class   = None
    serializer_class   = serializers.BranchSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'address']

    def get_queryset(self):
        user     = self.request.user
        queryset = self.queryset.all()
        queryset = queryset.filter(branch = user.branch) if user.branch else queryset
        return queryset
    
    def list(self, request, *args, **kwargs):
        if libs.is_csv_response(request):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return libs.get_csv_file_response(serializer.data, "branches.csv")
        return super().list(request, *args, **kwargs)
    
List_Branch = ListBranchAPI.as_view()






