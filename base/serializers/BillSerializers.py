from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType


from base import models
from base import libs
from base.serializers import ChildSerializer










class BillSerializer(serializers.ModelSerializer):
    children   = serializers.PrimaryKeyRelatedField(
        queryset = models.Child.objects.all(), 
        required = False,
        allow_empty = True,
        allow_null = True,
        many     = True,
        error_messages={
            'invalid': _('Invalid child ID.'),
            'does_not_exist': _('You must provide a valid child ID.'),
            'incorrect_type': _('child must be identified by an integer ID.')
        }
    ) 
    branch   = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    new_children = ChildSerializer(many = True, write_only=True, required=False)
    discount = serializers.CharField(required = False)
    class Meta:
        model = models.Bill
        fields = [
            'id',
            'cash',
            'instapay',
            'visa',
            'is_subscription',
            'subscription',
            'time_price',
            'products_price',
            'children',
            'new_children',
            'discount',
            'discount_value',
            'discount_type',
            'branch',
            'product_bills_set',
            'is_active',
            'is_allowed_age',
            'hour_price',
            'half_hour_price',
            'total_price',
            'spent_time',
            'children_count',
            'money_unbalance',
            'finished',
            'created',
            'updated',
            'created_by',
            'finished_by',
        ]
        read_only_fields = [
            'subscription',
            'discount_value',
            'discount_type',
            'product_bills_set',
            'is_active',
            'is_allowed_age',
            'hour_price',
            'half_hour_price',
            'total_price',
            'spent_time',
            'children_count',
            'money_unbalance',
            'finished',
            'created',
            'updated',
            'created_by',
            'finished_by',
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            if request.user.branch and request.user.branch != instance.branch:
                raise PermissionDenied(_("You Do Not have the permission to access this data"))
        data = super().to_representation(instance)
        if instance.is_active:
            data['spent_time']  = libs.calculate_timesince(instance.created)
            data["time_price"]  = libs.calculate_time_price(data['spent_time'], instance.hour_price, instance.half_hour_price) if not instance.is_subscription else 0
            data["total_price"] = Decimal(data["time_price"]) + Decimal(instance.products_price)
        created_by = instance.created_by
        finished_by = instance.finished_by
        calculations_updated_by = instance.calculations_updated_by
        branch = instance.branch
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        data['finished_by'] = finished_by.username if finished_by else None
        data['finished_by_id'] = finished_by.id if finished_by else None
        data['calculations_updated_by'] = calculations_updated_by.username if calculations_updated_by else None
        data['calculations_updated_by_id'] = calculations_updated_by.id if calculations_updated_by else None
        data['branch'] = branch.name if branch else None
        data['branch_id'] = branch.id if branch else None
        first_child = instance.children.all().first() if instance.children.exists() else None
        data['first_child'] = first_child.name if first_child else None
        data['first_phone'] = None
        if first_child:
            first_phone = first_child.child_phone_numbers_set.first() if first_child.child_phone_numbers_set.exists() else None
            data['first_phone'] = first_phone.phone_number.value if first_phone else None
        if instance.is_subscription:
            data['subscription'] = {
                'name'  : instance.subscription.name,
                'hours' : instance.subscription.hours
            }
        else:
            data.pop('subscription', None)

        data['children'] = []
        data['first_child'] = instance.children.all().first().name if instance.children.exists() else None
        for child in instance.children.all():
            child_data = {
                "id" : child.id,
                "name" : child.name,
                'phone_numbers' : []
            }
            for phone_data in child.child_phone_numbers_set.all():
                child_data['phone_numbers'].append({
                    'phone_number': phone_data.phone_number.value , 
                    'relationship': phone_data.relationship  ,
                })
            data['children'].append(child_data)

        merged_products          = []
        merged_retunred_products = []

        for product_bill in instance.product_bills_set.all():
            for pbp in product_bill.products.all():
                product = pbp.product_object
                if not product:
                    continue  # skip if product is missing

                name = getattr(product, 'name', 'Unnamed')
                unit_price = getattr(product, 'price', 0)
                quantity = pbp.quantity
                total_price = unit_price * quantity

                existing = next((item for item in merged_products if item['name'] == name), None)
                if existing:
                    existing['quantity'] += quantity
                    existing['total_price'] += total_price
                else:
                    merged_products.append({
                        'name': name,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': total_price
                    })
                    
            for pbp in product_bill.returned_products.all():
                product = pbp.product_object
                if not product:
                    continue  # skip if product is missing

                name = getattr(product, 'name', 'Unnamed')
                created_by = getattr(product, 'created_by', None)
                unit_price = getattr(product, 'price', 0)
                created = getattr(product, 'created', 'undefined')
                quantity = pbp.quantity
                total_price = unit_price * quantity
                
                merged_retunred_products.append({
                    'name': name,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'created_by': created_by.username if created_by else None,
                    'created_by_id': created_by.id if created_by else None,
                    'created': created,
                })
                    


        data['product_bills_set']          = merged_products
        data['returned_product_bills_set'] = merged_retunred_products
        
        data['discount']    = instance.discount.name if instance.discount else None
        data['discount_id'] = instance.discount.id   if instance.discount else None

        return data
        
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
    
    def validate_discount(self, value):
        obj = models.Discount.objects.filter(name = value).first()
        if not obj:
            raise ValidationError(_("Couldn't find a discount available to this branch with the given credentials."))
        return obj
    
    def validate_time_price(self, value):
        user = self.context['request'].user
        if value < 0: 
            raise ValidationError(_("Time Price can not be negative"))
        if user.role == 'reception':
            raise PermissionDenied(_("You do not have the permission to set the bill Time Price"))
        return value 
        
    def validate_products_price(self, value):
        user = self.context['request'].user
        if value < 0: 
            raise ValidationError(_("Cafe Price can not be negative"))
        if user.role == 'reception':
            raise PermissionDenied(_("You do not have the permission to set the bill Cafe Price"))
        return value 
    
    def validate_branch(self, value):
        request = self.context['request']
        if request.user    and    request.user.branch    and    value != request.user.branch:
            raise PermissionDenied(_("You can not create a bill with a different branch"))
        return value

    def validate_children(self, value):
        if value == []:
            raise ValidationError(_("Children list can not be empty"))
        child_ids = []
        for child in value:
            if child.is_active:
                raise ValidationError(_("Child {name} is currently registered in another bill").format(name=child.name))
            elif child.id in child_ids:
                raise ValidationError(_("You tried to add the same child more than once"))
            else:
                child_ids.append(child.id)
        return value
    
    

    def validate(self, attrs):
        discount  = attrs.get('discount', [])
        branch    = attrs.get('branch', [])
        if discount    and    branch    and    branch not in discount.branches.all():
            raise ValidationError(_("Couldn't find a discount available to this branch with the given credentials."))
        return super().validate(attrs)
    





    def create(self, validated_data):
        validated_data.pop('products_price', None)
        validated_data.pop('time_price', None)
        validated_data.pop('is_active', None)
        validated_data.pop('instapay', None)
        validated_data.pop('visa', None)
        validated_data.pop('cash', None)

        user                             = self.context['request'].user
        validated_data['created_by']     = user
        is_subscription                  = validated_data.get('is_subscription', False)
        branch                           = validated_data.get('branch')
        children                         = validated_data.get('children', [])
        discount                         = validated_data.pop('discount', None)
        request_new_children             = validated_data.pop('new_children', [])

        with transaction.atomic():

            for child_data in request_new_children:
                serializer = ChildSerializer(data=child_data, context=self.context)
                serializer.is_valid(raise_exception=True)
                child_instance = serializer.save()
                children.append(child_instance)

            validated_data['children_count'] = len(children)
            validated_data['children']       = children

            if is_subscription:
                if validated_data['children_count'] != 1:
                    raise ValidationError(_("Subscription bill cannot have more than one child"))
                child = children[0]
                subscription_instance = child.subscriptions_set.order_by('-created').first()
                # Ensure the child has a valid subscription
                if not subscription_instance    or    not subscription_instance.is_active :
                    raise ValidationError(_("The Child {name} has no current active subscription").format(name = child.name))
                # Ensure the child is allowed to visit the branch
                if not subscription_instance.subscription.is_multi_access:
                    if branch != subscription_instance.branch:
                        raise ValidationError(_("The Child {name} is not allowed to visit this branch").format(name=child.name))
                elif branch not in subscription_instance.subscription.usable_in_branches.all():
                    raise ValidationError(_("The Child {name} is not allowed to visit this branch").format(name=child.name))
                validated_data['subscription'] = subscription_instance

            validated_data['discount_value'] = discount.value if discount else 0
            validated_data['discount_type']  = discount.type  if discount else None
            validated_data['discount']       = discount       if discount else None
            time_price_instance              = branch.hour_prices_set.filter(children_count = validated_data['children_count']).first()

            if not time_price_instance:
                raise ValidationError(_("There is no hour prices found for {children_count} children in this branch.").format(children_count = validated_data['children_count']))
            
            validated_data["hour_price"]       = libs.apply_discount_to_price(time_price_instance.hour_price, validated_data['discount_value'], validated_data['discount_type'])
            validated_data["half_hour_price"]  = libs.apply_discount_to_price(time_price_instance.half_hour_price, validated_data['discount_value'], validated_data['discount_type'])
            
            for child in validated_data.get('children', []):
                if (branch  and  libs.calculate_age_decimal(child.birth_date) < branch.allowed_age)  or  child.special_needs:
                    validated_data["is_allowed_age"] = False
                child.is_active = True
                child.save()
            
            return super().create(validated_data)
    






    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not instance.is_active:
            raise PermissionDenied(_("The bill is already closed"))
        
        if user    and    user.branch    and    instance.branch != user.branch:
            raise PermissionDenied(_("You can not close a bill from a different branch"))

        for child in instance.children.all():
            child.is_active = False
            child.save()

        cash      = validated_data.pop('cash', 0)
        visa      = validated_data.pop('visa', 0)
        instapay  = validated_data.pop('instapay', 0)
        validated_data.clear()

        validated_data['cash']         = cash
        validated_data['visa']         = visa
        validated_data['instapay']     = instapay
        validated_data['finished']     = timezone.now()
        validated_data['is_active']    = False
        validated_data['finished_by']  = user
        validated_data['spent_time']   = libs.calculate_timesince(instance.created)
        remaining_spent_time           = libs.calculate_subscription_time(validated_data['spent_time'], instance.subscription) if instance.is_subscription else validated_data['spent_time'] 
        validated_data['time_price']   = libs.calculate_time_price(remaining_spent_time, instance.hour_price, instance.half_hour_price)
        validated_data['total_price']  = instance.products_price + validated_data['time_price']
        if validated_data['cash'] + validated_data['visa'] + validated_data['instapay'] != validated_data['total_price']:
            raise ValidationError(_("Total price does not equal the money client paid"))
        instance                       = super().update(instance, validated_data)

        return instance