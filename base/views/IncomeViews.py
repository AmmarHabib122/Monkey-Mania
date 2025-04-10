from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import Coalesce

from base import serializers
from base import models
from base import permissions
from base import libs




class IncomeDateRangeView(APIView):
    role_access_list    = ['owner', 'admin', 'manager']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    def get(self, request):
        # Get date range from query params
        branch = libs.get_one_branch_id()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        
        if not is_date_range:
            raise ValidationError(_("Start and End dates must be provided together"))

        # Initialize totals dict
        income_data = {
            'branch' : branch.name,
            'bills_total': 0,
            'children_count': 0,
            'material_expenses_total': 0,
            'general_expenses_total': 0,
            'salaries_total': 0,
            'subscriptions_total': 0,
            'net_income': 0
        }

        # 1. Bills Income
        bills_query = models.Bill.objects.filter(branch = branch)
        bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, start_date, end_date)
        income_data['bills_total'] = bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0)
        )['total']
        income_data['children_count'] = bills_query.aggregate(
            total=Coalesce(Sum('children_count'), 0)
        )['total']

        # 2. Subscription Income
        subscriptions_query = models.SubscriptionInstance.objects.filter(branch = branch)
        subscriptions_query = libs.get_all_instances_in_a_date_range_query(subscriptions_query, start_date, end_date)
        income_data['subscriptions_total'] = subscriptions_query.aggregate(
            total=Coalesce(Sum('price'), 0)
        )['total']

        # 3. Material Expenses
        material_expenses_query = models.MaterialExpense.objects.filter(branch = branch)
        material_expenses_query = libs.get_all_instances_in_a_date_range_query(material_expenses_query, start_date, end_date)
        income_data['material_expenses_total'] = material_expenses_query.aggregate(
            total=Coalesce(Sum('total_price'), 0)
        )['total']

        # 4. General Expenses
        general_expenses_query = models.GeneralExpense.objects.filter(branch = branch)
        general_expenses_query = libs.get_all_instances_in_a_date_range_query(general_expenses_query, start_date, end_date)
        income_data['general_expenses_total'] = general_expenses_query.aggregate(
            total=Coalesce(Sum('total_price'), 0)
        )['total']

        # 5. Staff Salaries
        salaries_query = models.StaffSalary.objects.filter(branch = branch)
        salaries_query = libs.get_all_instances_in_a_date_range_query(salaries_query, start_date, end_date)
        income_data['salaries_total'] = salaries_query.aggregate(
            total=Coalesce(Sum('total_value'), 0)
        )['total']

        # Calculate net income
        income_data['net_income'] = (
            + income_data['bills_total'] 
            + income_data['subscriptions_total'] 
            - income_data['material_expenses_total'] 
            - income_data['general_expenses_total'] 
            - income_data['salaries_total']
        )

        return Response(income_data)
    









class IncomeDayView(APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    def get(self, request):
        # Get date range from query params
        branch = libs.get_one_branch_id()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        
        if not is_date_range    or   start_date != end_date:
            raise ValidationError(_("Start and End dates must be provided and be equal"))

        # Initialize totals dict
        income_data = {
            'bills_total': 0,
            'children_count': 0,
            'withdraws_total': 0,
            'subscriptions_total': 0,
            'cashier_total': 0,
            'delivered': 0,
            'was_in_cashier': 0,
        }

        # 1. Bills Income
        bills_query = models.Bill.objects.filter(branch = branch)
        bills_query = libs.get_all_instances_in_a_day_query(bills_query, start_date)
        income_data['bills_total'] = bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0)
        )['total']
        income_data['children_count'] = bills_query.aggregate(
            total=Coalesce(Sum('children_count'), 0)
        )['total']

        # 2. Subscription Income
        subscriptions_query = models.SubscriptionInstance.objects.filter(branch = branch)
        subscriptions_query = libs.get_all_instances_in_a_day_query(subscriptions_query, start_date)
        income_data['subscriptions_total'] = subscriptions_query.aggregate(
            total=Coalesce(Sum('price'), 0)
        )['total']

        # 3. Staff withdraw
        withdraws_query = models.StaffWithdraw.objects.filter(branch = branch)
        withdraws_query = libs.get_all_instances_in_a_day_query(withdraws_query, start_date)
        income_data['withdraws_total'] = withdraws_query.aggregate(
            total=Coalesce(Sum('total_value'), 0)
        )['total']

        # 4. cashier    
        cashier_query = models.Cashier.objects.filter(branch = branch)
        cashier_query = libs.get_all_instances_in_a_day_query(cashier_query, start_date)
        current_day   = cashier_query.first()
        income_data['delivered'] = current_day.value if current_day else 0
        if income_data['delivered']:
            previous_day = models.Cashier.objects.filter(
                created__lt = current_day.created,  
                branch      = current_day.branch  
            ).order_by('-created').first()  
        income_data['was_in_cashier'] = previous_day.value if previous_day else 0
        income_data['cashier_total'] = (
            + income_data['was_in_cashier'] 
            + income_data['delivered_money']
            - income_data['withdraws_total']
        )

       

        return Response(income_data)