from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from django.db import transaction

from base import serializers
from base import models
from base import permissions
from base import libs


'''##############################OfferAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin']



class CreateOfferAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Offer.objects.all()
    serializer_class   = serializers.OfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Offer Created successfully")
        return response
Create_Offer = CreateOfferAPI.as_view()






class UpdateOfferAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Offer.objects.all()
    serializer_class   = serializers.OfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Offer Updated successfully")
        return response
Update_Offer = UpdateOfferAPI.as_view()




class GetOfferAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Offer.objects.all()
    serializer_class   = serializers.OfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_Offer = GetOfferAPI.as_view()







class ListOfferAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Offer.objects.all()
    serializer_class   = serializers.OfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name'] 
List_Offer = ListOfferAPI.as_view()




























'''##############################BranchOfferAPIs######################################'''
class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateBranchOfferAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.BranchOffer.objects.all()
    serializer_class   = serializers.BranchOfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Offer added to branch successfully")
        return response
Create_BranchOffer = CreateBranchOfferAPI.as_view()
       






class UpdateBranchOfferAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.BranchOffer.objects.all()
    serializer_class   = serializers.BranchOfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Offer branch data Updated successfully")
        return response
Update_BranchOffer = UpdateBranchOfferAPI.as_view()




class GetBranchOfferAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.BranchOffer.objects.all()
    serializer_class   = serializers.BranchOfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
    
Get_BranchOffer = GetBranchOfferAPI.as_view()







class ListBranchOfferAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.BranchOffer.objects.all()
    serializer_class   = serializers.BranchOfferSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['offer__name'] 

    def get_queryset(self):
        branch = libs.get_one_branch_id(self)
        query  = models.BranchOffer.objects.filter(branch = branch)
        return query
List_BranchOffer = ListBranchOfferAPI.as_view()






