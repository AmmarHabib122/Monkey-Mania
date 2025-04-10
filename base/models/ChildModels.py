from django.db import models

from base import libs



class Child(models.Model):
    name           = models.CharField(max_length = 150, unique = True)
    birth_date     = models.DateField()
    address        = models.CharField(max_length = 255)
    notes          = models.CharField(max_length = 255, null = True, blank = True)
    is_active      = models.BooleanField(default = False)
    special_needs  = models.BooleanField(default = False)
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)
    school         = models.ForeignKey('base.School', on_delete = models.SET_NULL, null = True, related_name = 'children_set')
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_children_set')
    #subscribion_id
    '''
        history
    '''
    @property
    def age(self):
        years, months, days = libs.calculate_age(self.birth_date)
        return {
            "years"  : years,
            "months" : months,
            "days"   : days,
        }
    


    def __str__(self):
        return self.name




class PhoneNumber(models.Model):
    value = models.CharField(max_length = 20, unique = True)
    def __str__(self):
        return self.value
    



class ChildPhoneNumber(models.Model):
    child         = models.ForeignKey('base.Child', on_delete = models.CASCADE, related_name = 'child_phone_numbers_set')
    phone_number  = models.ForeignKey('base.PhoneNumber', on_delete = models.CASCADE, related_name = 'child_phone_number_values_set')
    relationship  = models.CharField(max_length = 20)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['child', 'phone_number'],
                name   = 'unique_child_phone_number'
            )
        ]