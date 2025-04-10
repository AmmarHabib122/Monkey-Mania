from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta, time


from base import models




'''##############################SubscriptionSrializers######################################'''


class SubscriptionSerializer(serializers.ModelSerializer):
    usable_in_branches = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = False,
        many     = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    creatable_in_branches = serializers.PrimaryKeyRelatedField(
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
        model = models.Subscription
        fields = [
            'id',
            'name',
            'is_multi_access',
            'hours',
            'instance_duration',
            'sold_units',
            'price',
            'is_active',
            'usable_in_branches',
            'creatable_in_branches',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'is_multi_access',
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['creatable_in_branches'] = []
        for branch in instance.creatable_in_branches.all():
            data['creatable_in_branches'].append(branch.name)

        data['usable_in_branches'] = []
        for branch in instance.usable_in_branches.all():
            data['usable_in_branches'].append(branch.name)
        return data

    def validate_name(self, value):
        return value.lower()
    
    def validate_hours(self, value):
        if value < 0    or    float(value) % 0.5 != 0: 
            raise ValidationError(_("Subscription Hours Invalid value"))
        return value
    
    def validate_instance_duration(self, value):
        if value < 7: 
            raise ValidationError(_("Subscription Duration value must be more than or equal to 7 days"))
        return value
    
    def validate_price(self, value):
        if value < 0: 
            raise ValidationError(_("Subscription Price value can not be negative"))
        return value
    
    def validate_usable_in_branches(self, value):
        branch_ids = []
        for branch in value:
            if branch.id in branch_ids:
                raise ValidationError(_("You tried to add the same branch more than once"))
            else:
                branch_ids.append(branch.id)
        return value

    def validate_creatable_in_branches(self, value):
        if value == []:
            raise ValidationError(_("Branches list can not be empty"))
        branch_ids = []
        for branch in value:
            if branch.id in branch_ids:
                raise ValidationError(_("You tried to add the same branch more than once"))
            else:
                branch_ids.append(branch.id)
        return value
    




    def create(self, validated_data):
        validated_data.pop('is_active', None)
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



        




'''##############################SubscriptionInstanceSrializers######################################'''





class SubscriptionInstanceSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    subscription = serializers.PrimaryKeyRelatedField(
        queryset = models.Subscription.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid subscription ID.'),
            'does_not_exist': _('You must provide a valid subscription ID.'),
            'incorrect_type': _('subscription must be identified by an integer ID.')
        }
    ) 
    child = serializers.PrimaryKeyRelatedField(
        queryset = models.Child.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid child ID.'),
            'does_not_exist': _('You must provide a valid child ID.'),
            'incorrect_type': _('child must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.SubscriptionInstance
        fields = [
            'id',
            'cash',
            'instapay',
            'visa',
            'price',
            'hours',
            'expire_date',
            'subscription',
            'child',
            'branch',
            'is_active',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'hours',
            'expire_date',
            'price',
            'is_active',
            'created',
            'updated',
            'created_by',
        ]
        
    def validate_cash(self, value):
        if value < 0: 
            raise ValidationError(_("cash can not be negative"))
        return value

    def validate_instapay(self, value):
        if value < 0: 
            raise ValidationError(_("instapay can not be negative"))
        return value

    def validate_visa(self, value):
        if value < 0: 
            raise ValidationError(_("visa can not be negative"))
        return value
    
    def validate_expire_date(self, value):
        if value <= timezone.now().date():
            raise ValidationError(_("Expire-Date must be in the future."))
        return value
   
    def validate_branch(self, value):
        request = self.context['request']
        if request.user    and    request.user.branch    and    value != request.user.branch:
            raise PermissionDenied(_("You can not create a subscription with a different branch"))
        return value
    
    def validate_child(self, value):
        subscription = value.subscriptions_set.order_by('-created').first()
        if subscription    and    subscription.is_active:
            raise ValidationError(_("This child already has an active subscription"))
        return value
    
    def validate(self, attrs):
        branch       = attrs.get('branch')
        subscription = attrs.get('subscription')
        if branch    and    subscription    and    branch not in subscription.creatable_in_branches.all():
            raise PermissionDenied('This subscription is not allowed in this branch')
        return super().validate(attrs)
    




    def create(self, validated_data):
        user                           = self.context['request'].user
        cash                           = validated_data.get('cash', 0)
        visa                           = validated_data.get('visa', 0)
        instapay                       = validated_data.get('instapay', 0)
        validated_data['created_by']   = user
        validated_data['expire_date']  = timezone.now().date() + timedelta(days = validated_data['subscription'].instance_duration)
        validated_data['hours']        = validated_data['subscription'].hours
        validated_data['price']        = validated_data['subscription'].price
        if cash + visa + instapay  != validated_data['price']:
            raise ValidationError(_("The money Paid does not equal the price of the subscription"))
        validated_data['subscription'].sold_units += 1
        validated_data['subscription'].save()
        instance = super().create(validated_data)

        if instance.cash > 0:
            bill_content_type = ContentType.objects.get_for_model(instance)
            models.Cashier.objects.create(
                transaction_type   = bill_content_type,  
                transaction_id     = instance.id,
                branch             = instance.branch,
                value              = instance.cash,
                created_by         = user
            )
        return instance
    


    def update(self, instance, validated_data):
        user                           = self.context['request'].user
        cash                           = validated_data.get('cash')
        difference_in_cash             = cash - instance.cash if cash else 0
        cash                           = validated_data.get('cash', instance.cash)
        visa                           = validated_data.get('visa', instance.visa)
        instapay                       = validated_data.get('instapay', instance.instapay)

        if cash + visa + instapay  != instance.price:
            raise ValidationError(_("The money Paid does not equal the price of the subscription"))
        
        if difference_in_cash != 0:
            subscription_content_type = ContentType.objects.get_for_model(instance)
            models.Cashier.objects.create(
                transaction_type   = subscription_content_type,  
                transaction_id     = instance.id,
                branch             = instance.branch,
                value              = difference_in_cash,
                created_by         = user
            )
        return super().update(instance, validated_data)



        
