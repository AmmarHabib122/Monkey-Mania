from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from datetime import date, datetime, time, timedelta
from django.db.models import Sum, IntegerField, DecimalField

from base import serializers
from base import models
from base import permissions
from base import libs


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']


class CsvAnalyticsFile(RoleAccessList, APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    pagination_class    = None
    
    def get(self, request):
        branches  = libs.get_branch_ids(self)
        type      = request.query_params.get("type")
        start_date, end_date, is_date_range = libs.get_date_range(self)
        
        
        if type == 'phone_number':
            query = models.PhoneNumber.objects.all()
            if is_date_range   and   start_date == end_date:
                query = libs.get_all_instances_in_a_day_query(query, start_date)
            elif is_date_range:
                query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
            data = serializers.PhoneNumberSerializer(query, many = True).data
            return libs.get_csv_file_response(data, 'phone_numbers.csv', ['value', 'created'])
        
        
        elif type == 'products_sales':
            data = []
            products_sales = {}
            query    = models.ProductBill.objects.filter(bill__branch__in = branches) if branches != ['all'] else models.ProductBill.objects.all()
            
            if is_date_range   and   start_date == end_date:
                query = libs.get_all_instances_in_a_day_query(query, start_date)
            elif is_date_range:
                query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
            
            for record in query:
                for pbp in record.products.all():
                    product = pbp.product_object
                    if not product:
                        continue 
                    products_sales[product.name] = products_sales.get(product.name, 0) + pbp.quantity
            data.append(products_sales)
            # return libs.get_csv_file_response(data, 'products_sales.csv')
            return Response(data)
        else:
            raise ValidationError(_('Allowed values for type are ["phone_number", "products_sales", "bills_children_count"]'))
Get_CsvAnalyticsFile = CsvAnalyticsFile.as_view()
    





class CsvAnalyticsAllowedTypes(APIView):
    permission_classes  = [permissions.Authenticated]
    pagination_class    = None
    
    def get(self, request):
        allowed_types = [
            'phone_number',
            'products_sales',
            'bills_children_count',
        ]
        return Response(allowed_types)
        
Get_CsvAnalyticsAllowedTypes = CsvAnalyticsAllowedTypes.as_view()
