from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception', 'waiter']






class CreateProductBillAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.ProductBill.objects.all()
    serializer_class   = serializers.ProductBillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Cafe Bill Created successfully")
        return response
Create_ProductBill = CreateProductBillAPI.as_view()






class UpdateProductBillAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.ProductBill.objects.all()
    serializer_class   = serializers.ProductBillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
    
    #only patch requests
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        requestData = request.data.copy()
        returned_products = requestData.get('returned_products', None)
        if not returned_products:
            raise ValidationError(_("Returned Products Must be Provided"))
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'returned_products': returned_products}, partial=kwargs['partial'])
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        responseData = serializer.data
        responseData['message'] = _("Cafe Bill Updated successfully")
        return Response(responseData)
    
Update_ProductBill = UpdateProductBillAPI.as_view()




class GetProductBillAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.ProductBill.objects.all()
    serializer_class   = serializers.ProductBillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_queryset(self):
        queryset = self.queryset.all()
        if self.request.user.branch:
            queryset = queryset.filter(bill__branch = self.request.user.branch)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        response   = super().retrieve(request, *args, **kwargs)
        bill       = models.Bill.objects.get(id = response.data.get('bill'))
        if not bill.is_active    and    request.user.role in ['waiter', 'reception']:
                raise PermissionDenied(_("You do not have the permission to access this data"))
        return response
Get_ProductBill = GetProductBillAPI.as_view()





class ListActiveProductBillAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.ProductBill.objects.filter(bill__is_active = True).order_by('-id')
    pagination_class   = None
    serializer_class   = serializers.ProductBillSerializer
    role_access_list   = ['owner', 'admin', 'manager', 'reception', 'waiter']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['bill__children__name', 'table_number', 'bill_number'] 

    def get_queryset(self):
        branches = libs.get_branch_ids(self)
        queryset = super().get_queryset().filter(bill__branch__in = branches) if branches != ['all'] else super().get_queryset()
        return queryset
List_ActiveProductBill = ListActiveProductBillAPI.as_view()








class ListProductBillAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.ProductBill.objects.all().order_by('-id')
    serializer_class   = serializers.ProductBillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['bill__children__name', 'table_number', 'bill_number'] 

    def get_queryset(self):
        branches = libs.get_branch_ids(self)
        query    = super().get_queryset().filter(bill__branch__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
List_ProductBill = ListProductBillAPI.as_view()






