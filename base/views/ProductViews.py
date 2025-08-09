from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView


from base import serializers
from base import models
from base import permissions
from base import libs


'''##############################ProductAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin']



class CreateProductAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Product.objects.all()
    serializer_class   = serializers.ProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Product Created successfully")
        return response
Create_Product = CreateProductAPI.as_view()






class UpdateProductAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Product.objects.all()
    serializer_class   = serializers.ProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Product Updated successfully")
        return response
Update_Product = UpdateProductAPI.as_view()




class GetProductAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Product.objects.all()
    serializer_class   = serializers.ProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_Product = GetProductAPI.as_view()







class ListProductAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Product.objects.all()
    serializer_class   = serializers.ProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['layer1', 'layer2', 'layer3'] 
List_Product = ListProductAPI.as_view()




























'''##############################BranchProductAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateBranchProductAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.BranchProduct.objects.all()
    serializer_class   = serializers.BranchProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Product added to branch successfully")
        return response
Create_BranchProduct = CreateBranchProductAPI.as_view()
       






class UpdateBranchProductAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.BranchProduct.objects.all()
    serializer_class   = serializers.BranchProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Product branch data Updated successfully")
        return response
Update_BranchProduct = UpdateBranchProductAPI.as_view()




class GetBranchProductAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.BranchProduct.objects.all()
    serializer_class   = serializers.BranchProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
    
Get_BranchProduct = GetBranchProductAPI.as_view()







class ListBranchProductAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.BranchProduct.objects.all()
    serializer_class   = serializers.BranchProductSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['product__layer1', 'product__layer2', 'product__layer3'] 

    def get_queryset(self):
        layer1 = self.request.query_params.get("layer1", None)
        layer2 = self.request.query_params.get("layer2", None)
        branch = libs.get_one_branch_id(self)
        if layer1  and  layer2:
            query  = super().get_queryset().filter(branch = branch, product__layer1=layer1, product__layer2=layer2)
        elif layer1:
            query  = super().get_queryset().filter(branch = branch, product__layer1=layer1)
        else: 
            query  = super().get_queryset().filter(branch = branch) 
        return query
List_BranchProduct = ListBranchProductAPI.as_view()







class ListBranchProductLayer1(APIView):
    permission_classes  = [permissions.Authenticated]
    def get(self, request):
        branch = libs.get_one_branch_id(self)
        layer1_values = models.BranchProduct.objects.filter(branch=branch).values_list('product__layer1', flat=True).distinct()
        return Response(layer1_values)
List_BranchProductLayer1 = ListBranchProductLayer1.as_view()





class ListBranchProductLayer2(APIView):
    permission_classes  = [permissions.Authenticated]
    def get(self, request):
        layer1 = self.request.query_params.get("layer1", None)
        if not layer1:
            raise ValidationError (_("layer 1 must be provided"))
        branch = libs.get_one_branch_id(self)
        layer2_values = models.BranchProduct.objects.filter(branch=branch, product__layer1=layer1).values_list('product__layer2', flat=True).distinct()
        return Response(layer2_values)
List_BranchProductLayer2 = ListBranchProductLayer2.as_view()




class ListBranchProductLayer3(APIView):
    permission_classes  = [permissions.Authenticated]
    def get(self, request):
        layer1 = self.request.query_params.get("layer1", None)
        layer2 = self.request.query_params.get("layer2", None)
        if not layer1  or  not layer2:
            raise ValidationError (_("layer 1 and 2 must be provided"))
        branch = libs.get_one_branch_id(self)
        layer3_values = models.BranchProduct.objects.filter(branch=branch, product__layer1=layer1, product__layer2=layer2).values_list('product__layer3', flat=True).distinct()
        return Response(layer3_values)
List_BranchProductLayer3 = ListBranchProductLayer3.as_view()