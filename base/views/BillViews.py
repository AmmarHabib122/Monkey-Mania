from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from decimal import Decimal


from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']






class CreateBillAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Bill.objects.all()
    serializer_class   = serializers.BillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Bill Created successfully")
        return response
Create_Bill = CreateBillAPI.as_view()




class CloseBillAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Bill.objects.all()
    serializer_class   = serializers.BillSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        data = request.data.copy()
        for key in data.keys():
            if key not in ['cash', 'visa', 'instapay']:
                raise ValidationError(_("Wrong data for closing the bill"))
        response                 = super().update(request, *args, **kwargs)
        response.data['message'] = _("Bill Closed successfully")
        return response

Close_Bill = CloseBillAPI.as_view()







class ApplyDiscountBillAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Bill.objects.all()
    serializer_class   = serializers.BillSerializer
    role_access_list   = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        discount = request.data.get('discount')
        if not discount:
            raise ValidationError(_("Discount must be provided"))
        
        discount_instance = models.Discount.objects.filter(name = discount).first()
        if not discount_instance    or    instance.branch not in discount_instance.branches.all():
            raise ValidationError(_("Couldn't find a discount available to this branch with the given credentials."))
        
        instance.discount_value = discount_instance.value
        instance.discount_type  = discount_instance.type 
        
        if instance.is_active:
            instance.hour_price      = libs.apply_discount_to_price(instance.hour_price, instance.discount_value, instance.discount_type)
            instance.half_hour_price = libs.apply_discount_to_price(instance.half_hour_price, instance.discount_value, instance.discount_type)
        else:
            instance.time_price  = libs.apply_discount_to_price(instance.time_price, instance.discount_value, instance.discount_type)
            instance.total_price = instance.products_price + instance.time_price

        instance.save()
        data = serializers.BillSerializer(instance).data
        data['message'] = _("Discount Applied successfully")
        return Response(data)
Apply_Discount_Bill = ApplyDiscountBillAPI.as_view()




class GetBillAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Bill.objects.all()
    serializer_class   = serializers.BillSerializer
    role_access_list   = ['owner', 'admin', 'manager', 'reception', 'waiter']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        instance = super().get_object()
        if self.request.user.branch    and   instance.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        
        if instance.is_active:
            instance.time_spent  = libs.calculate_timesince(instance.created)
            instance.time_price  = libs.calculate_time_price(instance.time_spent, instance.hour_price, instance.half_hour_price) if not instance.is_subscription else 0
            instance.total_price = Decimal(instance.time_price) + Decimal(instance.products_price)
        elif self.request.user.role in ['waiter', 'reception']:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return instance

Get_Bill = GetBillAPI.as_view()





class ListActiveBillAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Bill.objects.filter(is_active = True)
    serializer_class   = serializers.BillSerializer
    role_access_list    = ['owner', 'admin', 'manager', 'reception', 'waiter']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['children__name', 'children__child_phone_numbers_set__phone_number__value'] 

    def get_queryset(self):
        branches  = libs.get_branch_ids(self)
        query     = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        return query
List_ActiveBill = ListActiveBillAPI.as_view()









class ListBillAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Bill.objects.all()
    serializer_class   = serializers.BillSerializer
    role_access_list    = ['owner', 'admin', 'manager']
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['children__name', 'children__child_phone_numbers_set__phone_number__value'] 

    def get_queryset(self):
        branches  = libs.get_branch_ids(self)
        query     = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
List_Bill = ListBillAPI.as_view()






