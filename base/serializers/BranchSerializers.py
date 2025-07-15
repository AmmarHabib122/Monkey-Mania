from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.db import transaction


from base import models
from base import libs


class HourPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HourPrice
        fields = [
            'id',
            'children_count',
            'hour_price',
            'half_hour_price',
        ]
    
    # Disable automatic UniqueTogetherValidator execution
    def run_validators(self, value):
        request = self.context.get('request')
        if not request    or    (request   and   request.method == 'POST'):   
            for validator in self.validators.copy():
                if isinstance(validator, serializers.UniqueTogetherValidator):
                    self.validators.remove(validator)
        return super().run_validators(value)

    def validate_children_count(self, value):
        if value <= 0: 
            raise ValidationError(_("Children-Count can not be negative or equal to zero"))
        return value
    
    def validate_hour_price(self, value):
        if value <= 0: 
            raise ValidationError(_("Hour-Price can not be negative or equal to zero"))
        return value
    
    def validate_half_hour_price(self, value):
        if value <= 0: 
            raise ValidationError(_("Half-Hour-Price can not be negative or equal to zero"))
        return value










class BranchSerializer(serializers.ModelSerializer):
    hour_prices_set = HourPriceSerializer(many = True)
    
    class Meta:
        model = models.Branch
        fields = [
            'id',
            'name',
            'address',
            'indoor',
            'allowed_age',
            'delay_allowed_time',
            'delay_fine_interval',
            'delay_fine_value',
            'created',
            'updated',
            'created_by',
            'manager',
            'hour_prices_set',
        ]
        read_only_fields = [
            'created',
            'updated',
            'created_by',
        ]
        
    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            if request.user.branch and request.user.branch != instance:
                raise PermissionDenied(_("You Do Not have the permission to access this data"))
        data = super().to_representation(instance)
        created_by = instance.created_by
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        data['hour_prices_set'] = HourPriceSerializer(instance.hour_prices_set.all(), many=True).data
        return data
    



    def vlidate_name(self, value):
        return value.lower()

    def validate_allowed_age(self, value):
        if value <= 0: 
            raise ValidationError(_("Age can not be negative or equal to zero"))
        return value

    def validate_manager(self, value):
        if value.role in ['waiter', 'reception']:
            raise ValidationError(_("You can only set a user with a manager role or higher to the branch manager field."))
        return value
    
    def validate_delay_allowed_time(self, value):
        if value <= 0: 
            raise ValidationError(_("Allowed Delay Minutes can not be negative or equal to zero"))
        return value
    
    def validate_delay_fine_interval(self, value):
        if value <= 0: 
            raise ValidationError(_("Delay Interval Minutes for the Fine can not be negative or equal to zero"))
        return value
    
    def validate_delay_fine_value(self, value):
        if value <= 0    or    value > 5: 
            raise ValidationError(_("Delay Fine value must be between zero and 5 days"))
        return value

    
    def validate(self, attrs):
        # Check for duplicate children_count in hour_prices
        hour_prices     = attrs.get('hour_prices_set', [])
        children_counts = [hp['children_count'] for hp in hour_prices]

        if len(children_counts) != len(set(children_counts)):
            raise ValidationError(_("Each children count must be unique per branch."))
        return attrs

    


    def create(self, validated_data):
        user                         = self.context['request'].user
        validated_data['created_by'] = user
        request_hour_prices          = validated_data.pop('hour_prices_set')
        manager                      = validated_data.pop('manager', None)
        instance                     = super().create(validated_data)
        hour_prices_list             = []

        for data in request_hour_prices:
            hour_prices_list.append(
                models.HourPrice(
                    children_count   = data['children_count'],
                    hour_price       = data['hour_price'],
                    half_hour_price  = data['half_hour_price'],
                    branch           = instance,
                )
            )
        models.HourPrice.objects.bulk_create(hour_prices_list)
        instance.save()
        return instance
    
    


    def update(self, instance, validated_data):
        user                = self.context['request'].user
        request_hour_prices = validated_data.pop('hour_prices_set', None)
        hour_prices_list    = []
        manager             = validated_data.get('manager')

        if    manager    and     manager.branch != instance   and    manager.role == "manager":
            raise ValidationError(_("You can not set a user from another branch to be the manager of this branch."))
        instance  = super().update(instance, validated_data)
        
        if request_hour_prices:
            for data in request_hour_prices:
                hour_price_instance = models.HourPrice.objects.filter(branch = instance, children_count = data['children_count'])
                if hour_price_instance.exists():
                    hour_price_instance                 = hour_price_instance.first()
                    hour_price_instance.hour_price      = data['hour_price']
                    hour_price_instance.half_hour_price = data['half_hour_price']
                    hour_price_instance.save()
                else:
                    hour_prices_list.append(
                        models.HourPrice(
                            children_count   = data['children_count'],
                            hour_price       = data['hour_price'],
                            half_hour_price  = data['half_hour_price'],
                            branch           = instance,
                        )
                    )
        models.HourPrice.objects.bulk_create(hour_prices_list)
        instance.save()
        return instance