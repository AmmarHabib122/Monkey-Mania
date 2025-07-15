from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions
from base import libs


'''##############################MaterialAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin']



class CreateMaterialAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Material.objects.all()
    serializer_class   = serializers.MaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Material Created successfully")
        return response
Create_Material = CreateMaterialAPI.as_view()






class UpdateMaterialAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Material.objects.all()
    serializer_class   = serializers.MaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Material Updated successfully")
        return response
Update_Material = UpdateMaterialAPI.as_view()




class GetMaterialAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Material.objects.all()
    serializer_class   = serializers.MaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_Material = GetMaterialAPI.as_view()







class ListMaterialAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Material.objects.all()
    serializer_class   = serializers.MaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name'] 
List_Material = ListMaterialAPI.as_view()




























'''##############################BranchMaterialAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateBranchMaterialAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.BranchMaterial.objects.all()
    serializer_class   = serializers.BranchMaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Material added to branch successfully")
        return response
Create_BranchMaterial = CreateBranchMaterialAPI.as_view()






class UpdateBranchMaterialAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.BranchMaterial.objects.all()
    serializer_class   = serializers.BranchMaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Material Branch data Updated successfully")
        return response
Update_BranchMaterial = UpdateBranchMaterialAPI.as_view()




class GetBranchMaterialAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.BranchMaterial.objects.all()
    serializer_class   = serializers.BranchMaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
    
Get_BranchMaterial = GetBranchMaterialAPI.as_view()







class ListBranchMaterialAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.BranchMaterial.objects.all()
    serializer_class   = serializers.BranchMaterialSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['material__name'] 

    def get_queryset(self):
        branches = libs.get_branch_ids(self)
        query    = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        return queryset
List_BranchMaterial = ListBranchMaterialAPI.as_view()






