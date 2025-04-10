from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.utils import timezone

from base import models






class DiscountSerializer(serializers.ModelSerializer):
    branches = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        many     = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.Discount
        fields = [
            'id',
            'name',
            'value',
            'type',
            'expire_date',
            'is_active',
            'branches',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'is_active',
            'created',
            'updated',
            'created_by',
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_data_branches = []
        for branch_id in data['branches']:
            branch = models.Branch.objects.get(id = branch_id)
            new_data_branches.append(branch.name)
        data['branches'] = new_data_branches
        return data

    def validate_name(self, value):
        return value.lower()
    
    def validate_value(self, value):
        if value < 0: 
            raise ValidationError(_("Discount value can not be negative"))
        return value
    
    def validate_branches(self, value):
        if value == []:
            raise ValidationError(_("Branches list can not be empty"))
        branch_ids = []
        for branch in value:
            if branch.id in branch_ids:
                raise ValidationError(_("You tried to add the same branch more than once"))
            else:
                branch_ids.append(branch.id)
        return value
    
    def validate_type(self, value):
        allowed_values = ['percentage', 'fixed', 'new value']
        if value not in allowed_values:
            raise ValidationError(_("Discount allowed types are {allowed_values}.").format(allowed_values = allowed_values))
        return value.lower()
    
    def validate_expire_date(self, value):
        if value <= timezone.now().date():
            raise ValidationError(_("Expire-Date must be in the future."))
        return value
    
    def validate(self, attrs):
        value =  attrs.get('value')
        type  =  attrs.get('type ')
        if type == 'percentage'   and    value > 1:
            raise ValidationError(_("Discount value for percentage type must be between 0 and 1"))
        return super().validate(attrs)



    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



        


        