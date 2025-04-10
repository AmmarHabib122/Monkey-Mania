# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError, PermissionDenied
# from django.utils.translation import gettext as _

# from base import models






# class SchoolSerializer(serializers.ModelSerializer):
#     day = serializers.PrimaryKeyRelatedField(
#         queryset = models.Day.objects.all(), 
#         required = True,
#         error_messages={
#             'invalid': _('Invalid day ID.'),
#             'does_not_exist': _('You must provide a valid day ID.'),
#             'incorrect_type': _('day must be identified by an integer ID.')
#         }
#     ) 
#     class Meta:
#         model = models.School
#         fields = [
#             'id',
#             'name',
#             'day',
#             'total_income',
#             'delivered_cash',
#             'cash',
#             'visa',
#             'instapay',
#             'pre_shift_cash',
#             'is_active',
#             'bills_money_unbalance',
#             'created',
#             'updated',
#             'created_by',
#         ]
#         read_only_fields = [
#             'name',
#             'day',
#             'total_income',
#             'is_active',
#             'bills_money_unbalance',
#             'created',
#             'updated',
#             'created_by',
#         ]
        
#         def validate_cash(self, value):
#             if value < 0: 
#                 raise ValidationError(_("cash can not be negative"))
#             return value
        
#         def validate_visa(self, value):
#             if value < 0: 
#                 raise ValidationError(_("visa can not be negative"))
#             return value
        
#         def validate_instapay(self, value):
#             if value < 0: 
#                 raise ValidationError(_("instapay can not be negative"))
#             return value
        
#         def validate_pre_shift_cash(self, value):
#             if value < 0: 
#                 raise ValidationError(_("pre-shift-cash can not be negative"))
#             return value
        
#         def validate_delivered_cash(self, value):
#             if value < 0: 
#                 raise ValidationError(_("delivered-cash can not be negative"))
#             return value

#     def validate(self, attrs):
#         delivered_cash   = attrs.get('delivered_cash', None)
#         cash             = attrs.get('cash', None)
#         if cash and delivered_cash:
#             if delivered_cash > cash:
#                 raise ValidationError(_("How the Delievered cash is bigger than the whole day cash?!!!"))
#         return super().validate(attrs)



#     def create(self, validated_data):
#         user                           = self.context['request'].user
#         day                            = validated_data.pop('day', None)
#         validated_data.clear()
#         if day:
#             validated_data['day']      = day
#         validated_data['created_by']   = user
#         validated_data['name']         = f"{day.name} {user.username}"
#         instance                       = super().create(validated_data)
#         instance.update_pre_shift_cash()
#         return instance
    


#     def update(self, instance, validated_data):
#         return super().update(instance, validated_data)



        