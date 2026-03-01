from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import date
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import timedelta, time, datetime
from decimal import Decimal
import pandas as pd
import csv
from io import StringIO
from django.http import HttpResponse


from base import models



roles_power = {
    "owner"     : 1000,
    "admin"     : 800,
    "manager"   : 600,
    "reception" : 400,
    "waiter"    : 200,   
}
'''
    below 700 does not have a branch
    below 500 cannot add users or perform manager actions
'''
def get_role_power(user):
    return roles_power[user.role]







def get_branch_ids(self):
    user = self.request.user
    if user.branch:
        branches = [user.branch.id]
    else :
        branches = self.request.query_params.getlist("branch_id", [])
        if not branches:
            raise ValidationError (_("Branch id must be provided"))
        if branches != ['all']:
            try:
                branches = [int(branch) for branch in branches]
                for branch in branches:
                    models.Branch.objects.get(id = branch)
            except:
                raise ValidationError (_("Invalid Branch id"))
        
    return branches



def get_one_branch_id(self):
    user = self.request.user
    if user.branch:
        branch = user.branch.id
    else:
        branch = self.request.query_params.get("branch_id", None)
        try:
            if branch:
                branch = int(branch)
                models.Branch.objects.get(id = branch)
            else:
                raise ValidationError (_("Invalid Branch id"))
        except:
            raise ValidationError (_("Invalid Branch id"))
    return branch



def get_lower_roles(user):
    user_power    = roles_power.get(user.role, 0)
    allowed_roles = [role for role, power in roles_power.items() if power < user_power]
    return allowed_roles




def validate_phone_number(phone_number):
    if not phone_number.isdigit():
        raise ValidationError(_("Phone number must contain only digits."))
    if len(phone_number) != 11:
        raise ValidationError(_("Phone number must be exactly 11 digits long."))
    return phone_number


def calculate_age(birth_date):
    today = date.today()
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    # Adjust for negative months/days
    if days < 0:
        months -= 1
        days += 30  # Simplified adjustment (use calendar for exact days)
    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def calculate_age_decimal(birth_date):
    today = date.today()
    age_days = (today - birth_date).days
    age_years = age_days / 365.2425
    return round(age_years, 2)


def validate_image(value):
    allowed_extensions = ['jpg', 'jpeg', 'png']
    extension = value.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(_(f'Unsupported file extension {extension} . Allowed: {allowed_extensions}'))

    # Validate file size (e.g., 2MB max)
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Image file is too large! Max size allowed: {max_size / (1024 * 1024)}MB")
    
    return value



def calculate_money_unbalance(total_money, *payment_types):
    money_unbalance = sum(payment_types) - total_money
    return money_unbalance




def calculate_timesince(start_time):
    spent_time = (timezone.now() - start_time).total_seconds() // 60  # time in minutes
    return spent_time




def calculate_time_price(spent_time, hour_price, half_hour_price):
    spent_time  = max(spent_time - 15, 0)                 #extra 15 minutes allowed for clients without charges
    hours       = Decimal(spent_time // 60); 
    spent_time %= 60
    time_price  = hours * hour_price
    if spent_time > 30:
        time_price += hour_price
    elif spent_time > 0:
        time_price += half_hour_price   
    time_price  = time_price if time_price > 0 else 0
    return Decimal(time_price)



def calculate_subscription_time(spent_time, subscription_instance):
    '''
        spent time is in minutes but subscription_instance.remaining_hours is in hours
    '''
    spent_time = Decimal(spent_time)
    spent_time = max(spent_time - 15, 0)                 #extra 15 minutes allowed for clients without charges
    
    if subscription_instance.remaining_hours > spent_time / 60:
        hours                        = spent_time // 60; 
        spent_time                  %= 60
        subscription_instance.remaining_hours -= hours
        if spent_time > 30:
            subscription_instance.remaining_hours -= Decimal("1.00")
        elif spent_time > 0:
            subscription_instance.remaining_hours -= Decimal("0.50")
        spent_time                   = 0

    else:
        spent_time -= (subscription_instance.remaining_hours * 60)
        spent_time += 15 #add the extra 15 minutes allowed for clients again is they will be removed in calculating time price function
        subscription_instance.remaining_hours = Decimal("0")

    subscription_instance.save()
    return spent_time
        






def apply_discount_to_price(original_price, discount_value, discount_type):
    discounted_price_dict = {
        None         : original_price,
        'percentage' : original_price * (1 - discount_value),
        'fixed'      : (original_price - discount_value) if discount_value < original_price else 0,
        'new value'  : discount_value,
    }
    discounted_price  = discounted_price_dict[discount_type]
    discounted_price -= discounted_price % 5
    return discounted_price




def get_all_instances_in_a_day_query(query, date):
    app_tz = timezone.get_current_timezone()
    start_of_day = timezone.make_aware(datetime.combine(date, time(7, 0)), app_tz)
    end_of_day = start_of_day + timedelta(days=1)
    return query.filter(created__range=(start_of_day, end_of_day))


def get_all_instances_in_a_date_range_query(query, start_date, end_date):
    app_tz = timezone.get_current_timezone()
    start_dt = timezone.make_aware(datetime.combine(start_date, time(7, 0)), app_tz)
    end_dt = timezone.make_aware(datetime.combine(end_date + timedelta(days=1), time(7, 0)), app_tz)
    return query.filter(created__range=(start_dt, end_dt))






def get_all_instances_in_a_month_based_on_created_field(instance, query):
    model        = instance.__class__
    created_date = instance.created.date()
    created_time = instance.created.time()
    
    # Check if 'created' is on the first day of the month and time is before 7 AM
    if created_date.day == 1 and created_time < time(7, 0):
        # Move to previous month
        if created_date.month == 1:
            start_date = date(created_date.year - 1, 12, 1)
        else:
            start_date = date(created_date.year, created_date.month - 1, 1)
        
    else:
        # Normal case: get the first day of the current month based on 'created'
        start_date = created_date.replace(day=1)

    #End date should be the last day of the current month
    if start_date.month == 12:
        end_date = date(start_date.year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(start_date.year, start_date.month + 1, 1) - timedelta(days=1)
    # Use the existing function to get all instances in the month's range based on 'created'
    query = get_all_instances_in_a_date_range_query(query, start_date, end_date)
    
    return query




def get_date_range(self):
    start_date        = self.request.query_params.get("start_date")
    end_date          = self.request.query_params.get("end_date")
    if start_date and end_date:
        start_date        = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date          = datetime.strptime(end_date, "%Y-%m-%d").date()
        is_date_range     = True
        if start_date > end_date:
            raise ValidationError(_("Start date cannot be bigger than the end date"))
    elif start_date or end_date:
        raise ValidationError(_("Start and End dates must be provided together"))
    else:
        is_date_range = False         #to know that the user want all table records not filtered by date interval
    return start_date, end_date, is_date_range



def get_csv_file_records(request, required_columns=[]):
    file = request.FILES.get('file')
    if not file:
        raise ValidationError(_("Csv file must be provided"))
    if not file.name.endswith('.csv'):
        raise ValidationError(_("The file provided must be in .csv format"))
    file = pd.read_csv(file)
    missing_columns = [col for col in required_columns if col not in file.columns]
    if missing_columns:
        raise ValidationError(_("Wrong column format, The correct Format is {required_columns}").format(required_columns=required_columns))
    records = []
    for row in file.to_dict(orient='records'):
        clean_row = {k: v for k, v in row.items() if pd.notna(v) and str(v).strip() != ''}
        records.append(clean_row)     
    return records
                
            
            
def is_csv_response(request):
    is_csv = request.query_params.get("is_csv_response")
    if is_csv is None:
        return False
    if str(is_csv).lower() in ["true", "1", "yes"]:
        return True
    if str(is_csv).lower() in ["false", "0", "no"]:
        return False
    raise ValidationError(_("Only True or False are allowed for is_csv_response parameter"))
    


def send_csv_file_response(data, filename="data.csv", columns=None):
    df = pd.DataFrame(data, columns=columns if columns else None)
    buffer = StringIO()
    df.to_csv(buffer, index=False, encoding='utf-8-sig')
    response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response 





def query_filter_by_single_field_from_filter_dict(request, query, filter_dict):
    filter = request.query_params.get("filter")
    if filter in filter_dict.keys():
        return filter_dict[filter](query)
    elif filter is None  or  filter == "":
        return query
    else:
        raise ValidationError(_("Invalid filter value"))

            
