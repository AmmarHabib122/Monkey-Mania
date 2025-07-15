from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from datetime import date, timedelta
from django.db.models import Sum, IntegerField, DecimalField

from base import serializers
from base import models
from base import permissions
from base import libs




class DashboardSatistics(APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    def get(self, request):
        #add a start_date and end_date to the request as today and yesterday
        today = date.today()
        yesterday = today - timedelta(days=1)
        query = request._request.GET.copy()
        query["start_date"] = today  # Default start date, can be changed
        query["end_date"] = today    # Default end date, can be changed
        request._request.GET = query

        branch = libs.get_one_branch_id(self)
        today_start, today_end, is_date_range = libs.get_date_range(self)
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end   = today_end   - timedelta(days=1)

        # Initialize response dict
        dashboard_statistics = {
            'todays_kids_sales': 0,
            'kids_sales_difference_from_yesterday': 0,

            'todays_cafe_sales': 0,
            'cafe_sales_difference_from_yesterday': 0,

            'todays_children_count': 0,
            'children_count_difference_from_yesterday': 0,

            'todays_subscriptions_sales': 0,
            'todays_subscriptions_count': 0,

            'todays_staff_withdraws_total': 0,
            'todays_staff_requested_withdraw_count': 0,
            
            'todays_money_unbalance': 0,
        }

        # 1. Today Total Sales
        bills_query = models.Bill.objects.filter(branch = branch) if branch else models.Bill.objects.all()
        bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, today_start, today_end)
        today_kids_sales = bills_query.aggregate(
            total=Coalesce(Sum('time_price'), 0, output_field=DecimalField())
        )['total']
        todays_children_count = bills_query.aggregate(
            total=Coalesce(Sum('children_count'), 0)
        )['total']
        todays_money_unbalance = sum(bill.money_unbalance for bill in bills_query)
        dashboard_statistics['todays_kids_sales'] = today_kids_sales
        dashboard_statistics['todays_money_unbalance'] = str(todays_money_unbalance) if todays_money_unbalance < 0 else "+" + str(todays_money_unbalance)
        dashboard_statistics['todays_children_count'] = todays_children_count

        # 2. Yesterday Total Sales
        bills_query = models.Bill.objects.filter(branch = branch) if branch else models.Bill.objects.all()
        bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, yesterday_start, yesterday_end)
        yesterday_kids_sales = bills_query.aggregate(
            total=Coalesce(Sum('time_price'), 0, output_field=DecimalField())
        )['total']
        yeseterdays_children_count = bills_query.aggregate(
            total=Coalesce(Sum('children_count'), 0)
        )['total']
        if yesterday_kids_sales > 0:
            kids_sales_difference_from_yesterday = (today_kids_sales - yesterday_kids_sales) / yesterday_kids_sales * 100 
            dashboard_statistics['kids_sales_difference_from_yesterday'] = str(kids_sales_difference_from_yesterday) + "%" if kids_sales_difference_from_yesterday < 0 else "+" + str(kids_sales_difference_from_yesterday) + "%"
        else :
            dashboard_statistics['kids_sales_difference_from_yesterday'] = "Not defined"
        children_count_difference_from_yesterday = todays_children_count - yeseterdays_children_count
        dashboard_statistics['children_count_difference_from_yesterday'] = str(children_count_difference_from_yesterday) if children_count_difference_from_yesterday < 0 else "+" + str(children_count_difference_from_yesterday)

        # 3. Today Created Subscriptions count and sales
        subscriptions_query = models.SubscriptionInstance.objects.filter(branch = branch) if branch else models.SubscriptionInstance.objects.all()
        subscriptions_query = libs.get_all_instances_in_a_date_range_query(subscriptions_query, today_start, today_end)
        dashboard_statistics['todays_subscriptions_count'] = subscriptions_query.count()
        dashboard_statistics['todays_subscriptions_sales'] = subscriptions_query.aggregate(
            total=Coalesce(Sum('price'), 0, output_field=DecimalField())
        )['total']

        # 4. Today Cafe Cales
        product_bills_query = models.ProductBill.objects.filter(bill__branch = branch) if branch else models.ProductBill.objects.all()
        product_bills_query = libs.get_all_instances_in_a_date_range_query(product_bills_query, today_start, today_end)
        todays_product_bills_sales = product_bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0, output_field=DecimalField())
        )['total']
        dashboard_statistics['todays_cafe_sales'] = todays_product_bills_sales

        # 5. Yesterday Cafe Cales
        product_bills_query = models.ProductBill.objects.filter(bill__branch = branch) if branch else models.ProductBill.objects.all()
        product_bills_query = libs.get_all_instances_in_a_date_range_query(product_bills_query, yesterday_start, yesterday_end)
        yesterdays_product_bills_sales = product_bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0, output_field=DecimalField())
        )['total']
        if yesterdays_product_bills_sales > 0:
            product_bills_difference_from_yesterday = (todays_product_bills_sales - yesterdays_product_bills_sales) / yesterdays_product_bills_sales * 100
            dashboard_statistics['cafe_sales_difference_from_yesterday'] = str(product_bills_difference_from_yesterday) + "%" if product_bills_difference_from_yesterday < 0 else "+" + str(product_bills_difference_from_yesterday) + "%"
        else : 
            dashboard_statistics['cafe_sales_difference_from_yesterday'] = "Not defined"
            
        # 6. Staff Withdraws
        staff_withdraws_query = models.StaffWithdraw.objects.filter(branch = branch) if branch else models.StaffWithdraw.objects.all()
        staff_withdraws_query = libs.get_all_instances_in_a_date_range_query(staff_withdraws_query, today_start, today_end)
        dashboard_statistics['todays_staff_requested_withdraw_count'] = staff_withdraws_query.values('staff').distinct().count()
        dashboard_statistics['todays_staff_withdraws_total'] = staff_withdraws_query.aggregate(
            total=Coalesce(Sum('value'), 0, output_field=DecimalField())
        )['total']

        return Response(dashboard_statistics)
Get_DashboardStatistics = DashboardSatistics.as_view()
    









class IncomeDayView(APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    def get(self, request):
        # Get date range from query params
        branch = libs.get_one_branch_id()
        today_start, today_end, is_date_range = libs.get_date_range(self)
        
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