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






class CreateDiscountAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Discount.objects.all()
    serializer_class   = serializers.DiscountSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Discount Created successfully")
        return response
Create_Discount = CreateDiscountAPI.as_view()






class UpdateDiscountAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Discount.objects.all()
    serializer_class   = serializers.DiscountSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Discount Updated successfully")
        return response
Update_Discount = UpdateDiscountAPI.as_view()




class GetDiscountAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Discount.objects.all()
    serializer_class   = serializers.DiscountSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   not obj.branches.filter(id = self.request.user.branch.id).exists():
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj

Get_Discount = GetDiscountAPI.as_view()







class ListDiscountAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Discount.objects.all().order_by('-id')
    serializer_class   = serializers.DiscountSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name'] 
    
    def get_queryset(self):
        branches  = libs.get_branch_ids(self)
        query     = super().get_queryset().filter(branches__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
    def list(self, request, *args, **kwargs):
        if libs.is_csv_response(request):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return libs.get_csv_file_response(serializer.data, "discounts.csv")
        return super().list(request, *args, **kwargs)
    
List_Discount = ListDiscountAPI.as_view()






