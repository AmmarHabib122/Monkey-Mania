from django.db import models
import math
from decimal import Decimal

from base import libs




class Staff(models.Model):
    name                  = models.CharField(max_length = 150, unique = True)
    phone_number          = models.CharField(max_length = 20, unique = True)
    address               = models.CharField(max_length = 255)
    salary                = models.DecimalField(max_digits = 11, decimal_places = 2)
    shift_hours           = models.DecimalField(max_digits = 3, decimal_places = 1)
    is_active             = models.BooleanField(default = True)
    allowed_absence_days  = models.IntegerField()
    created               = models.DateTimeField(auto_now_add = True)
    updated               = models.DateTimeField(auto_now = True)
    images                = models.ManyToManyField('base.Image', related_name = "staff_images_set")
    branch                = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'staff_set')
    created_by            = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_staff_set')

    @property
    def day_value(self):
        return round(self.salary / 30, 2)

    @property
    def minute_value(self):
        return round(self.day_value / self.shift_hours / 60, 4)

    def __str__(self):
        return self.name







class StaffWithdraw(models.Model):
    staff          = models.ForeignKey('base.Staff', on_delete = models.CASCADE, related_name = 'withdraws_set')
    branch         = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'branch_withdraw_set')
    value          = models.DecimalField(max_digits = 14, decimal_places = 2)
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_withdraw_set')
    










class StaffFine(models.Model):
    staff          = models.ForeignKey('base.Staff', on_delete = models.CASCADE, related_name = 'fines_set')
    branch         = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'branch_fines_set')
    reason         = models.CharField(max_length = 255)
    value          = models.DecimalField(max_digits = 4, decimal_places = 2)   #number of days
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_fines_set')















class StaffSalary(models.Model):
    staff                         = models.ForeignKey('base.Staff', on_delete = models.CASCADE, related_name = 'salaries_set')
    branch                        = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'branch_salaries_set')
    delay_time                    = models.IntegerField()
    minus_time                    = models.IntegerField()
    over_time                     = models.IntegerField()
    absence_days                  = models.IntegerField()
    allowed_absence_days          = models.IntegerField()
    delay_allowed_time            = models.IntegerField()
    delay_fine_interval           = models.IntegerField()
    delay_fine_value              = models.DecimalField(max_digits = 2, decimal_places = 2)
    shift_hours                   = models.IntegerField()
    original_salary_value         = models.DecimalField(max_digits = 15, decimal_places = 2)
    bonus_value                   = models.IntegerField()  
    total_value                   = models.DecimalField(max_digits = 15, decimal_places = 2)
    created                       = models.DateTimeField(auto_now_add = True)
    updated                       = models.DateTimeField(auto_now = True)
    created_by                    = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_salaries_set')




    @property
    def original_salary_day_value(self):
        return self.original_salary_value / Decimal(30)

    @property
    def original_salary_minute_value(self):
        return round(self.original_salary_day_value / self.shift_hours / Decimal(60), 4)

    @property
    def over_time_value(self):
        return self.over_time * self.original_salary_minute_value

    @property
    def minus_time_value(self):
        return self.minus_time * self.original_salary_minute_value * -1

    @property
    def delay_time_value(self):
        if self.delay_time > self.delay_allowed_time:
            fine_intervals = math.ceil(
               (self.delay_time - self.delay_allowed_time) / self.delay_fine_interval
            )
            return fine_intervals * (self.original_salary_day_value * self.delay_fine_value) * -1
        return 0

    @property
    def absence_days_value(self):
        return (self.allowed_absence_days - self.absence_days) * self.original_salary_day_value
    
    @property
    def withdraws(self):
        query = libs.get_all_instances_in_a_month_based_on_created_field(self, self.staff.withdraws_set.all())
        total = query.aggregate(total=models.Sum('value'))['total'] or 0
        return total * -1
    
    @property
    def fines(self):
        query = libs.get_all_instances_in_a_month_based_on_created_field(self, self.staff.fines_set.all())
        total = query.aggregate(total=models.Sum('value'))['total'] or 0
        return total * self.original_salary_day_value * -1

    # @property
    # def total_value(self):
    #     total_value = sum([
    #         self.original_salary_value,
    #         self.over_time_value,
    #         self.bonus_value,
    #         self.absence_days_value,
    #         self.minus_time_value,
    #         self.delay_time_value,
    #         self.fines,
    #         self.withdraws,
    #     ]) 
    #     total_value = (total_value + 4) // 5 * 5    #round up to nearest 5
    #     return total_value