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


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']

class DashboardSatistics(RoleAccessList, APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    def get(self, request):
        #add a start_date and end_date to the request as today and yesterday
        today = date.today()
        yesterday = today - timedelta(days=1)
        query = request.GET.copy()
        query["start_date"] = today.strftime("%Y-%m-%d")  # Default start date, can be changed
        query["end_date"] = today.strftime("%Y-%m-%d")    # Default end date, can be changed
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
    



