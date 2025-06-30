from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
import math

from base import models
from base import libs




class StaffSerializer(serializers.ModelSerializer):
    is_user = serializers.BooleanField(default = False)
    branch  = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.Staff
        fields = [
            'id',
            'name',
            'phone_number',
            'allowed_absence_days',
            'address',
            'salary',
            'shift_hours',
            'day_value',
            'is_active',
            'images',
            'branch',
            'is_user',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'day_value',
            'images',
            'created',
            'updated',
            'created_by',
        ]
        
    
    def to_representation(self, instance):
        request = self.context.get('request')
        if    request    and    request.user.branch   and     request.user.branch != instance.branch:
            raise PermissionDenied(_("You Do Not have the permission to access this data"))
    
        data = super().to_representation(instance)
        data['images'] = [image.value.url for image in instance.images.all()] if instance.images.exists() else []
        return data





    def validate_name(self, value):
        return value.lower()
    
    def validate_salary(self, value):
        if value <= 0: 
            raise ValidationError(_("Salary can not be negative or equal to zero."))
        return value
    
    def validate_phone_number(self, value):
        libs.validate_phone_number(value)
        return value

    def validate_allowed_absence_days(self, value):
        if value >= 31:
            raise ValidationError(_("Allowed Absence Days value cannot be larger than 31"))
        return value
    
    def validate_shift_hours(self, value):
        if value > 12:
            raise ValidationError(_("Shift Hours value cannot be larger than 12 hour"))
        return value

    def validate_branch(self, value):
        request = self.context['request']
        if request.user.branch    and    value != request.user.branch:
            raise PermissionDenied(_("You Do not have the permission to assign staff to another branch"))
        if request.method.lower() != 'post':
            raise PermissionDenied(_("You Do not have the permission edit the branch field"))
        return value


    def validate(self, attrs):
        request    = self.context.get("request") 
        is_partial = request and request.method == "PATCH" 
        is_user    = attrs.pop('is_user', False)
        if    not is_user    and    not is_partial    and    attrs.get('branch') == None:
            raise ValidationError(_("Branch must be provided"))
        return super().validate(attrs)



    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        staff_branch                   = validated_data.get('branch')
        is_active                      = validated_data.pop('is_active', None)
        instance                       = super().create(validated_data)
        return instance
    

    def update(self, instance, validated_data):
        user     = self.context['request'].user
        if user.branch   and   instance.branch != user.branch:
            raise PermissionDenied(_("You Do not have the permission to manipulate other branches staff"))
        return super().update(instance, validated_data)



        

    









'''##############################StaffWithdrawSerializers######################################'''



class StaffWithdrawSerializer(serializers.ModelSerializer):
    staff  = serializers.PrimaryKeyRelatedField(
        queryset = models.Staff.objects.all(), 
        error_messages={
            'invalid': _('Invalid staff ID.'),
            'does_not_exist': _('You must provide a valid staff ID.'),
            'incorrect_type': _('staff must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.StaffWithdraw
        fields = [
            'id',
            'staff',
            'value',
            'branch',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'branch',
            'created',
            'updated',
            'created_by',
        ]

    
    def validate_value(self, value):
        if value <= 0: 
            raise ValidationError(_("Withdraw value can not be negative or equal to zero"))
        return value

    def validate_staff(self, value):
        request   = self.context['request']
        if request.user.branch    and    value.branch != request.user.branch:
            raise PermissionDenied(_("You can not add a withdraw to this staff member"))
        return value

    

    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        validated_data['branch']       = validated_data['staff'].branch
        instance                       =  super().create(validated_data)
        withdraw_content_type          = ContentType.objects.get_for_model(instance)
        models.Cashier.objects.create(
            transaction_type   = withdraw_content_type,  
            transaction_id     = instance.id,
            branch             = instance.branch,
            value              = instance.value * -1,
            created_by         = user
        )
        return instance
    


    def update(self, instance, validated_data):
        user                = self.context['request'].user
        value               = validated_data.get('value')
        difference_in_value = value - instance.value if value else 0

        if user    and    user.branch    and   instance.branch != user.branch:
            raise PermissionDenied(_("You can not update a staff withdraw from another branch"))

        instance = super().update(instance, validated_data)

            
        if difference_in_value != 0:
            withdraw_content_type = ContentType.objects.get_for_model(instance)
            models.Cashier.objects.create(
                transaction_type   = withdraw_content_type,  
                transaction_id     = instance.id,
                branch             = instance.branch,
                value              = instance.value * -1,
                created_by         = user
            )

        return instance






        












'''##############################StaffFineSerializers######################################'''



class StaffFineSerializer(serializers.ModelSerializer):
    staff  = serializers.PrimaryKeyRelatedField(
        queryset = models.Staff.objects.all(), 
        error_messages={
            'invalid': _('Invalid staff ID.'),
            'does_not_exist': _('You must provide a valid staff ID.'),
            'incorrect_type': _('staff must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.StaffFine
        fields = [
            'id',
            'staff',
            'reason',
            'value',
            'branch',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'branch',
            'created',
            'updated',
            'created_by',
        ]

    
    def validate_value(self, value):
        if value <= 0 or value >= 10: 
            raise ValidationError(_("Fine days value must be above zero and below 10"))
        return value

    def validate_staff(self, value):
        request   = self.context['request']
        if request.user.branch    and    value.branch != request.user.branch:
            raise PermissionDenied(_("You can not add a fine to this staff member"))
        return value

    

    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        validated_data['branch']       = validated_data['staff'].branch
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        user   = self.context['request'].user
        if user    and    user.branch    and   instance.branch != user.branch:
            raise PermissionDenied(_("You can not update a staff fine from another branch"))
        return super().update(instance, validated_data)











'''##############################StaffSalarySerializers######################################'''



class StaffSalarySerializer(serializers.ModelSerializer):
    withdraws = serializers.SerializerMethodField()
    fines = serializers.SerializerMethodField()
    staff  = serializers.PrimaryKeyRelatedField(
        queryset = models.Staff.objects.all(), 
        error_messages={
            'invalid': _('Invalid staff ID.'),
            'does_not_exist': _('You must provide a valid staff ID.'),
            'incorrect_type': _('staff must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.StaffSalary
        fields = [
            'id',
            'staff',
            'delay_time',
            'minus_time',
            'over_time',
            'absence_days',
            'bonus_value',

            #read only
            'branch',
            'allowed_absence_days',
            'delay_allowed_time',
            'delay_fine_interval',
            'delay_fine_value',
            'shift_hours',
            'original_salary_value',
            'original_salary_day_value',
            'original_salary_minute_value',
            'over_time_value',
            'minus_time_value',
            'delay_time_value',
            'absence_days_value',
            'total_value',
            'withdraws',
            'fines',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'allowed_absence_days',
            'delay_allowed_time',
            'delay_fine_interval',
            'delay_fine_value',
            'shift_hours',
            'original_salary_value',
            'original_salary_day_value',
            'original_salary_minute_value',
            'over_time_value',
            'minus_time_value',
            'delay_time_value',
            'absence_days_value',
            'total_value',
            'withdraws',
            'fines',
            'branch',
            'created',
            'updated',
            'created_by',
        ]


    def get_withdraws(self, obj):
        return obj.withdraws

    def get_fines(self, obj):
        return obj.fines

    def validate_over_time(self, value):
        if value < 0: 
            raise ValidationError(_("Over Time value can not be negative"))
        return value
    
    def validate_minus_time(self, value):
        if value < 0: 
            raise ValidationError(_("Minus Time value can not be negative"))
        return value
    
    def validate_delay_time(self, value):
        if value < 0: 
            raise ValidationError(_("Delay Time value can not be negative"))
        return value
    
    def validate_absence_days(self, value):
        if value < 0    or    value > 30: 
            raise ValidationError(_("Absence Days value can not be negative or above 30"))
        return value
    
    def validate_bonus_value(self, value):
        if value < 0 : 
            raise ValidationError(_("Bonus value can not be negative"))
        return value
    

    def validate_staff(self, value):
        request   = self.context['request']
        if request.user.branch    and    value.branch != request.user.branch:
            raise PermissionDenied(_("You can not add a salary to this staff member"))
        return value

    

    def create(self, validated_data):
        user                                            = self.context['request'].user
        validated_data['created_by']                    = user
        validated_data['branch']                        = validated_data['staff'].branch
        validated_data['delay_allowed_time']            = validated_data['branch'].delay_allowed_time
        validated_data['delay_fine_interval']           = validated_data['branch'].delay_fine_interval
        validated_data['delay_fine_value']              = validated_data['branch'].delay_fine_value
        validated_data['shift_hours']                   = validated_data['staff'].shift_hours
        validated_data['allowed_absence_days']          = validated_data['staff'].allowed_absence_days
        validated_data['original_salary_value']         = validated_data['staff'].salary
        instance                                        = super().create(validated_data)
        instance.total_value = (sum([
            instance.original_salary_value,
            instance.over_time_value,
            instance.bonus_value,
            instance.absence_days_value,
            instance.minus_time_value,
            instance.delay_time_value,
            instance.fines,
            instance.withdraws,
        ]) + 4) // 5 * 5 
        return instance
    







    def update(self, instance, validated_data):
        user   = self.context['request'].user
        if user    and    user.branch    and   instance.branch != user.branch:
            raise PermissionDenied(_("You can not update a staff salary from another branch"))

        if validated_data.get('absence_days'):
            validated_data['absence_days'] = max(0, validated_data['absence_days'] - instance.staff.allowed_absence_days)
        
        instance = super().update(instance, validated_data)
        instance.total_value = (sum([
            instance.original_salary_value,
            instance.over_time_value,
            instance.bonus_value,
            instance.absence_days_value,
            instance.minus_time_value,
            instance.delay_time_value,
            instance.fines,
            instance.withdraws,
        ]) + 4) // 5 * 5 
        return instance
    

