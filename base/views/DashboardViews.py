from rest_framework import generics
from rest_framework.views import APIView
from django.utils.translation import gettext as _
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from datetime import date, datetime, time, timedelta
from django.db.models import Sum, IntegerField, DecimalField, Count, Q

from base import serializers
from base import models
from base import permissions
from base import libs


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']

class DashboardSatistics(RoleAccessList, APIView):
    role_access_list    = ['owner', 'admin', 'manager', 'reception']
    permission_classes  = [permissions.Authenticated, permissions.RoleAccess]
    pagination_class    = None
    
    def get(self, request):
        today = date.today()
        if datetime.now().time() < time(7, 0):  # cleaner
            today -= timedelta(days=1)
        start_date        = request.query_params.get("start_date", None)
        end_date          = request.query_params.get("end_date", None)
        is_current_children_allowed = False
        if start_date and end_date:
            main_interval_start, main_interval_end, main_interval_is_date_range = libs.get_date_range(self)
        else:
            main_interval_start = today
            main_interval_end = today
            main_interval_is_date_range = False
            is_current_children_allowed = True
            
        #if main_interval is week 2 in october compare_interval will be week 1 in october
        compare_interval_end    = main_interval_start - timedelta(days = 1)
        compare_interval_start  = compare_interval_end - (main_interval_end - main_interval_start)
        
        branch = libs.get_branch_ids(self)
        
        # Initialize response dict that contains the value of the main interval and the compared interval
        dashboard_statistics = {
            'todays_kids_sales': 0,                              #main_interval data
            'kids_sales_difference_from_yesterday': 0,           #main_interval data comapred with the compare_interval data

            'todays_cafe_sales': 0,
            'cafe_sales_difference_from_yesterday': 0,

            'todays_children_count': 0,
            'children_count_difference_from_yesterday': 0,

            'todays_subscriptions_sales': 0,
            'subscriptions_sales_difference_from_yesterday': 0,

            'todays_staff_withdraws_total': 0,
            'todays_staff_requested_withdraw_count': 0,
            
            'todays_money_unbalance': 0,
            'money_unbalance_difference_from_yesterday': 0,
            
            'todays_cash': 0,
            'cash_difference_from_yesterday': 0,
            
            'todays_instapay': 0,
            'instapay_difference_from_yesterday': 0,
            
            'todays_visa': 0,
            'visa_difference_from_yesterday': 0,
        }

        # 1. main_interval bills && subscriptiions calculations
        bills_query = models.Bill.objects.filter(branch__in = branch) if branch != ["all"] else models.Bill.objects.all()
        bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, main_interval_start, main_interval_end)
        subscriptions_query = models.SubscriptionInstance.objects.filter(branch__in = branch) if branch != ["all"] else models.SubscriptionInstance.objects.all()
        subscriptions_query = libs.get_all_instances_in_a_date_range_query(subscriptions_query, main_interval_start, main_interval_end)
        
        todays_bills_query_sum_agg = bills_query.aggregate(
            children       = Coalesce(Sum('children_count'), 0),
            kids_sales     = Coalesce(Sum('time_price'), 0, output_field=DecimalField()),
            cash           = Coalesce(Sum('cash'), 0, output_field=DecimalField()),
            visa           = Coalesce(Sum('visa'), 0, output_field=DecimalField()),
            instapay       = Coalesce(Sum('instapay'), 0, output_field=DecimalField()),
        )
        todays_bills_query_count_agg = bills_query.aggregate(
            total_bills_count     = Count('id'),
            cash_bills_count      = Count('id', filter=Q(cash__gt=0)),
            visa_bills_count      = Count('id', filter=Q(visa__gt=0)),
            instapay_bills_count  = Count('id', filter=Q(instapay__gt=0)),
        )
        todays_subscripiton_query_sum_agg = subscriptions_query.aggregate(
            subscriptions_sales    = Coalesce(Sum('price'), 0, output_field=DecimalField()),
            cash                   = Coalesce(Sum('cash'), 0, output_field=DecimalField()),
            visa                   = Coalesce(Sum('visa'), 0, output_field=DecimalField()),
            instapay               = Coalesce(Sum('instapay'), 0, output_field=DecimalField()),
        )
        todays_subscripiton_query_count_agg = subscriptions_query.aggregate(
            total_subscriptions_count     = Count('id'),
            cash_subscriptions_count      = Count('id', filter=Q(cash__gt=0)),
            visa_subscriptions_count      = Count('id', filter=Q(visa__gt=0)),
            instapay_subscriptions_count  = Count('id', filter=Q(instapay__gt=0)),
        )
        todays_bills_query_sum_agg['cash']                         +=  todays_subscripiton_query_sum_agg['cash']
        todays_bills_query_sum_agg['visa']                         +=  todays_subscripiton_query_sum_agg['visa']
        todays_bills_query_sum_agg['instapay']                     +=  todays_subscripiton_query_sum_agg['instapay']
        todays_bills_query_sum_agg['money_unbalance']               = sum(bill.money_unbalance for bill in bills_query)
        todays_bills_query_count_agg['money_unbalance_bills_count'] = sum(1 for bill in bills_query if bill.money_unbalance > 0)
        
        dashboard_statistics['todays_kids_sales']           = f"{todays_bills_query_sum_agg['kids_sales']} ({todays_bills_query_count_agg['total_bills_count']})"
        dashboard_statistics['todays_money_unbalance']      = str(todays_bills_query_sum_agg['money_unbalance']) if todays_bills_query_sum_agg['money_unbalance'] < 0 else "+" + str(todays_bills_query_sum_agg['money_unbalance']) + f" ({todays_bills_query_count_agg['money_unbalance_bills_count']})"
        dashboard_statistics['todays_children_count']       = f"{todays_bills_query_sum_agg['children']} (current : {bills_query.filter(is_active = True).aggregate(total=Coalesce(Sum('children_count'), 0)) ['total']})" if is_current_children_allowed else f"{todays_bills_query_sum_agg['children']}"
        dashboard_statistics['todays_cash']                 = f"{todays_bills_query_sum_agg['cash']} ({todays_bills_query_count_agg['cash_bills_count'] + todays_subscripiton_query_count_agg['cash_subscriptions_count']})"
        dashboard_statistics['todays_visa']                 = f"{todays_bills_query_sum_agg['visa']} ({todays_bills_query_count_agg['visa_bills_count'] + todays_subscripiton_query_count_agg['visa_subscriptions_count']})"
        dashboard_statistics['todays_instapay']             = f"{todays_bills_query_sum_agg['instapay']} ({todays_bills_query_count_agg['instapay_bills_count'] + todays_subscripiton_query_count_agg['instapay_subscriptions_count']})"
        dashboard_statistics['todays_subscriptions_sales']  = f"{todays_subscripiton_query_sum_agg['subscriptions_sales']} ({todays_subscripiton_query_count_agg['total_subscriptions_count']})"


        # 2. compare_interval bills && subscriptiions calculations
        bills_query = models.Bill.objects.filter(branch__in = branch) if branch != ["all"] else models.Bill.objects.all()
        bills_query = libs.get_all_instances_in_a_date_range_query(bills_query, compare_interval_start, compare_interval_end)
        subscriptions_query = models.SubscriptionInstance.objects.filter(branch__in = branch) if branch != ["all"] else models.SubscriptionInstance.objects.all()
        subscriptions_query = libs.get_all_instances_in_a_date_range_query(subscriptions_query, compare_interval_start, compare_interval_end)
        
        yesterdays_bills_query_sum_agg = bills_query.aggregate(
            children       = Coalesce(Sum('children_count'), 0),
            kids_sales     = Coalesce(Sum('time_price'), 0, output_field=DecimalField()),
            cash           = Coalesce(Sum('cash'), 0, output_field=DecimalField()),
            visa           = Coalesce(Sum('visa'), 0, output_field=DecimalField()),
            instapay       = Coalesce(Sum('instapay'), 0, output_field=DecimalField()),
        )
        yesterdays_subscripiton_query_sum_agg = subscriptions_query.aggregate(
            subscriptions_sales    = Coalesce(Sum('price'), 0, output_field=DecimalField()),
            cash                   = Coalesce(Sum('cash'), 0, output_field=DecimalField()),
            visa                   = Coalesce(Sum('visa'), 0, output_field=DecimalField()),
            instapay               = Coalesce(Sum('instapay'), 0, output_field=DecimalField()),
        )
        yesterdays_bills_query_sum_agg['cash']           +=  yesterdays_subscripiton_query_sum_agg['cash']
        yesterdays_bills_query_sum_agg['visa']           +=  yesterdays_subscripiton_query_sum_agg['visa']
        yesterdays_bills_query_sum_agg['instapay']       +=  yesterdays_subscripiton_query_sum_agg['instapay']
        yesterdays_bills_query_sum_agg['money_unbalance'] = sum(bill.money_unbalance for bill in bills_query)
        # todays_bills_query_sum_agg['kids_sales'] = 3
        # yesterdays_bills_query_sum_agg['kids_sales'] = 1
        if yesterdays_bills_query_sum_agg['kids_sales'] > 0:
            kids_sales_difference_from_yesterday = round((todays_bills_query_sum_agg['kids_sales'] - yesterdays_bills_query_sum_agg['kids_sales']) / yesterdays_bills_query_sum_agg['kids_sales'] * 100, 2)
            if kids_sales_difference_from_yesterday < 0: 
                dashboard_statistics['kids_sales_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * kids_sales_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['kids_sales_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {kids_sales_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['kids_sales_difference_from_yesterday']     = f"لا يوجد مبيعات اطفال في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_bills_query_sum_agg['cash'] > 0:
            cash_difference_from_yesterday = round((todays_bills_query_sum_agg['cash'] - yesterdays_bills_query_sum_agg['cash']) / yesterdays_bills_query_sum_agg['cash'] * 100, 2)
            if cash_difference_from_yesterday < 0: 
                dashboard_statistics['cash_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * cash_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['cash_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {cash_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['cash_difference_from_yesterday']     = f"لا يوجد دفع بالكاش في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_bills_query_sum_agg['instapay'] > 0:
            instapay_difference_from_yesterday = round((todays_bills_query_sum_agg['instapay'] - yesterdays_bills_query_sum_agg['instapay']) / yesterdays_bills_query_sum_agg['instapay'] * 100, 2)
            if instapay_difference_from_yesterday < 0: 
                dashboard_statistics['instapay_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * instapay_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['instapay_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {instapay_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['instapay_difference_from_yesterday']     = f"لا يوجد دفع بالانستاباي في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_bills_query_sum_agg['visa'] > 0:
            visa_difference_from_yesterday = round((todays_bills_query_sum_agg['visa'] - yesterdays_bills_query_sum_agg['visa']) / yesterdays_bills_query_sum_agg['visa'] * 100, 2)
            if visa_difference_from_yesterday < 0: 
                dashboard_statistics['visa_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * visa_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['visa_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {visa_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['visa_difference_from_yesterday']     = f"لا يوجد دفع بالفيزا في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_subscripiton_query_sum_agg['subscriptions_sales'] > 0:
            subscriptions_sales_difference_from_yesterday = round((todays_subscripiton_query_sum_agg['subscriptions_sales'] - yesterdays_subscripiton_query_sum_agg['subscriptions_sales']) / yesterdays_subscripiton_query_sum_agg['subscriptions_sales'] * 100, 2)
            if subscriptions_sales_difference_from_yesterday < 0: 
                dashboard_statistics['subscriptions_sales_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * subscriptions_sales_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['subscriptions_sales_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {subscriptions_sales_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['subscriptions_sales_difference_from_yesterday']     = f"لا يوجد اشتراكات تم انشاؤها في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_bills_query_sum_agg['money_unbalance'] > 0:
            money_unbalance_difference_from_yesterday = round((todays_bills_query_sum_agg['money_unbalance'] - yesterdays_bills_query_sum_agg['money_unbalance']) / yesterdays_bills_query_sum_agg['money_unbalance'] * 100, 2)
            if money_unbalance_difference_from_yesterday < 0: 
                dashboard_statistics['money_unbalance_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * money_unbalance_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['money_unbalance_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {money_unbalance_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['money_unbalance_difference_from_yesterday']     = f"لا يوجد عدم توازن مالي في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        if yesterdays_bills_query_sum_agg['children'] > 0:
            children_count_difference_from_yesterday = todays_bills_query_sum_agg['children'] - yesterdays_bills_query_sum_agg['children']
            if children_count_difference_from_yesterday < 0: 
                dashboard_statistics['children_count_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * children_count_difference_from_yesterday} طفل"
            else :
                dashboard_statistics['children_count_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {children_count_difference_from_yesterday} طفل"
        else:
            dashboard_statistics['children_count_difference_from_yesterday']     = f"لا يوجد اطفال في الفترة من {compare_interval_start} الي {compare_interval_end}"
        

        # # 3. main_interval Created Subscriptions count and sales
        # subscriptions_query = models.SubscriptionInstance.objects.filter(branch__in = branch) if branch != ["all"] else models.SubscriptionInstance.objects.all()
        # subscriptions_query = libs.get_all_instances_in_a_date_range_query(subscriptions_query, main_interval_start, main_interval_end)
        # dashboard_statistics['todays_subscriptions_count'] = subscriptions_query.count()
        # dashboard_statistics['todays_subscriptions_sales'] = subscriptions_query.aggregate(
        #     total=Coalesce(Sum('price'), 0, output_field=DecimalField())
        # )['total']
        # dashboard_statistics['todays_cash'] += subscriptions_query.aggregate(
        #     total=Coalesce(Sum('cash'), 0, output_field=DecimalField())
        # )['total']
        # dashboard_statistics['todays_visa'] += subscriptions_query.aggregate(
        #     total=Coalesce(Sum('visa'), 0, output_field=DecimalField())
        # )['total']
        # dashboard_statistics['todays_instapay'] += subscriptions_query.aggregate(
        #     total=Coalesce(Sum('instapay'), 0, output_field=DecimalField())
        # )['total']

        # 4. main_interval Cafe Cales
        product_bills_query = models.ProductBill.objects.filter(bill__branch__in = branch) if branch != ["all"] else models.ProductBill.objects.all()
        product_bills_query = libs.get_all_instances_in_a_date_range_query(product_bills_query, main_interval_start, main_interval_end)
        todays_product_bills_sales = product_bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0, output_field=DecimalField())
        )['total']
        dashboard_statistics['todays_cafe_sales'] = f"{todays_product_bills_sales} ({product_bills_query.count()})"

        # 5. compare_interval Cafe Cales
        product_bills_query = models.ProductBill.objects.filter(bill__branch__in = branch) if branch != ["all"] else models.ProductBill.objects.all()
        product_bills_query = libs.get_all_instances_in_a_date_range_query(product_bills_query, compare_interval_start, compare_interval_end)
        yesterdays_product_bills_sales = product_bills_query.aggregate(
            total=Coalesce(Sum('total_price'), 0, output_field=DecimalField())
        )['total']
        
        if yesterdays_product_bills_sales > 0:
            product_bills_difference_from_yesterday = round((todays_product_bills_sales - yesterdays_product_bills_sales) / yesterdays_product_bills_sales * 100, 2)
            if product_bills_difference_from_yesterday < 0: 
                dashboard_statistics['cafe_sales_difference_from_yesterday'] = f"اقل من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {-1 * product_bills_difference_from_yesterday} في المية"
            else :
                dashboard_statistics['cafe_sales_difference_from_yesterday'] = f"اكثر من الفترة {compare_interval_start} الي {compare_interval_end} بحوالي {product_bills_difference_from_yesterday} في المية"
        else :
            dashboard_statistics['cafe_sales_difference_from_yesterday']     = f"لا يوجد مبيعات كافيه في الفترة من {compare_interval_start} الي {compare_interval_end}"
            
        # 6. Staff Withdraws
        staff_withdraws_query = models.StaffWithdraw.objects.filter(branch__in = branch) if branch != ["all"] else models.StaffWithdraw.objects.all()
        staff_withdraws_query = libs.get_all_instances_in_a_date_range_query(staff_withdraws_query, main_interval_start, main_interval_end)
        todays_staff_withdraws_total = staff_withdraws_query.aggregate(
            total=Coalesce(Sum('value'), 0, output_field=DecimalField())
        )['total']
        
        dashboard_statistics['todays_staff_requested_withdraw_count'] = f"عدد الموظفين اللي قامو بالسحب {staff_withdraws_query.values('staff').distinct().count()}"
        dashboard_statistics['todays_staff_withdraws_total'] = f"{todays_staff_withdraws_total} ({staff_withdraws_query.count()})"
        

        return Response(dashboard_statistics)
Get_DashboardStatistics = DashboardSatistics.as_view()
    



