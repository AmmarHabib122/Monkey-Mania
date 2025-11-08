from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from datetime import date, datetime, time, timedelta
from django.db.models import Sum, IntegerField, DecimalField
from django.db.models import OuterRef, Subquery

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
            bills_query = models.Bill.objects.all()
            if is_date_range   and   start_date == end_date:
                bills_query = libs.get_all_instances_in_a_day_query(bills_query, start_date)
            elif is_date_range:
                bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, start_date, end_date)
            
            children_query = models.Child.objects.all()
            if is_date_range   and   start_date == end_date:
                children_query = libs.get_all_instances_in_a_day_query(children_query, start_date)
            elif is_date_range:
                children_query = libs.get_all_instances_in_a_date_range_query(children_query, start_date, end_date) 
            
            filtered_children = []
            if branches != ['all']:
                for child in children_query:
                    first_bill = child.child_bills_set.order_by('created').first()
                    if first_bill.branch.id in branches:
                        filtered_children.append(child)
            else:
                filtered_children = children_query
                
                
                
            children_phone_numbers = models.ChildPhoneNumber.objects.filter(child__in=filtered_children)
            
            phone_numbers_qs = models.PhoneNumber.objects.filter(
                id__in=children_phone_numbers.values_list('phone_number_id', flat=True)
            )
            
            #refilter by date as we may have a created child within the interval but used an old number stored in the system            
            if is_date_range   and   start_date == end_date:
                phone_numbers_qs = libs.get_all_instances_in_a_day_query(phone_numbers_qs, start_date)
            elif is_date_range:
                phone_numbers_qs = libs.get_all_instances_in_a_date_range_query(phone_numbers_qs, start_date, end_date)
            
            data = serializers.PhoneNumberSerializer(phone_numbers_qs, many = True).data
            return libs.send_csv_file_response(data, 'phone_numbers.csv', ['value', 'created'])
        
        
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
            return libs.send_csv_file_response(data, 'products_sales.csv')
        
        
        elif type == 'bills_children_count':
            data = []
            bills_children_count = {}
            query    = models.Bill.objects.filter(branch__in = branches) if branches != ['all'] else models.Bill.objects.all()
            
            if is_date_range   and   start_date == end_date:
                query = libs.get_all_instances_in_a_day_query(query, start_date)
            elif is_date_range:
                query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
            
            for record in query:
                key = str(record.children_count) + " children"
                bills_children_count[key] = bills_children_count.get(key, 0) + record.children_count
            data.append(bills_children_count)
            return libs.send_csv_file_response(data, 'children_count.csv')
        
        
        elif type == 'discounts':
            data = []
            dicount_bills_count = {}
            discount_query = models.Discount.objects.all()
            for discount in discount_query:
                if is_date_range   and   start_date == end_date:
                    bills_query = libs.get_all_instances_in_a_day_query(discount.discount_bills_set.all(), start_date)
                elif is_date_range:
                    bills_query = libs.get_all_instances_in_a_date_range_query(discount.discount_bills_set().all(), start_date, end_date)
                dicount_bills_count[discount.name] = dicount_bills_count.get(discount.name, 0) + bills_query.count()
            data.append(dicount_bills_count)  
            return libs.send_csv_file_response(data, 'discounts.csv')
        
        else:
            raise ValidationError(_('Allowed values for type are ["phone_number", "products_sales", "bills_children_count", "discounts"]'))
        
Get_CsvAnalyticsFile = CsvAnalyticsFile.as_view()
    





class CsvAnalyticsAllowedTypes(APIView):
    permission_classes  = [permissions.Authenticated]
    pagination_class    = None
    
    def get(self, request):
        allowed_types = [
            'phone_number',
            'products_sales',
            'bills_children_count',
            'discounts',
        ]
        return Response(allowed_types)
        
Get_CsvAnalyticsAllowedTypes = CsvAnalyticsAllowedTypes.as_view()
