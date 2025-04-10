from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import libs
from base import permissions




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateCashierAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Cashier.objects.all()
    serializer_class   = serializers.CashierSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Dlieverd Money Created successfully")
        return response
Create_Cashier = CreateCashierAPI.as_view()








class ListCashierAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Cashier.objects.all()
    serializer_class   = serializers.CashierSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'address'] 

    def get_queryset(self):
        branch   = libs.get_one_branch_id(self)
        query    = super().get_queryset().filter(branch=branch)
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query

List_Cashier = ListCashierAPI.as_view()






