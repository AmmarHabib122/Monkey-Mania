from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.db import transaction

from base import models
from base.serializers import *




class CafeBillItemSerializer(serializers.ModelSerializer):
    branch_product = serializers.PrimaryKeyRelatedField(
        queryset     = models.BranchCafeProduct.objects.all(),
        required     = True,
        error_messages = {
            'invalid':        _('Invalid product ID.'),
            'does_not_exist': _('You must provide a valid product ID.'),
            'incorrect_type': _('product must be identified by an integer ID.')
        }
    )

    class Meta:
        model  = models.CafeBillItem
        fields = ['id', 'old_product_id', 'branch_product', 'quantity', 'notes']

    



class CafeBillReturnSerializer(serializers.ModelSerializer):
    branch_product = serializers.PrimaryKeyRelatedField(
        queryset     = models.BranchCafeProduct.objects.all(),
        required     = True,
        error_messages = {
            'invalid':        _('Invalid product ID.'),
            'does_not_exist': _('You must provide a valid product ID.'),
            'incorrect_type': _('product must be identified by an integer ID.')
        }
    )

    class Meta:
        model          = models.CafeBillReturn
        fields         = ['id', 'old_product_id', 'branch_product', 'quantity', 'created_by']
        read_only_fields = ['created_by']





class CafeBillSerializer(serializers.ModelSerializer):
    items   = CafeBillItemSerializer(many=True, required=True)
    returns = CafeBillReturnSerializer(many=True, required=False)
    bill    = serializers.PrimaryKeyRelatedField(
        queryset = models.Bill.objects.all(),
        required = True,
        error_messages = {
            'invalid':        _('Invalid bill ID.'),
            'does_not_exist': _('You must provide a valid bill ID.'),
            'incorrect_type': _('bill must be identified by an integer ID.')
        }
    )

    class Meta:
        model  = models.CafeBill
        fields = [
            'id',
            'bill_number',
            'table_number',
            'total_price',
            'take_away',
            'bill',
            'items',
            'returns',
            'created_by',
            'created',
            'updated',
        ]
        read_only_fields = [
            'bill_number', 
            'total_price', 
            'created_by', 
            'created', 
            'updated'
        ]


    def to_representation(self, instance):
        request    = self.context.get('request')
        data       = super().to_representation(instance)
        created_by = instance.created_by
        data['created_by']    = created_by.username if created_by else None
        data['created_by_id'] = created_by.id       if created_by else None
        bill = instance.bill
        data['first_child'] = bill.children.all().first().name if bill.children.exists() else None
        data['branch']      = bill.branch.name if bill.branch else None
        data['branch_id']   = bill.branch.id   if bill.branch else None

        # Process items
        new_items_data = []
        for item_data in data.get('items', []):
            product = item_data.get('product', {})
            if product:
                new_items_data.append({
                    'id':          product.get('id', None),
                    'unit_price':  product.get('price', 0),
                    'total_price': float(product.get('price', 0)) * float(item_data['quantity']),
                    'quantity':    item_data['quantity'],
                    'notes':       item_data['notes'],
                    'name':        product.get('name', 'Unknown Product'),
                })
        data['items'] = [i for i in new_items_data if i]

        # Process returns (only for non-waiter/reception roles)
        if request and request.user.role not in ['waiter', 'reception']:
            new_returns_data = []
            for return_data in data.get('returns', []):
                product = return_data.get('product', {})
                if product:
                    created_by_user = models.User.objects.filter(id=return_data['created_by']).first()
                    new_returns_data.append({
                        'id':             product.get('id', None),
                        'name':           product.get('name', 'Unknown Product'),
                        'quantity':       return_data['quantity'],
                        'created_by':     created_by_user.username if created_by_user else None,
                        'created_by_id':  created_by_user.id       if created_by_user else None,
                    })
            data['returns'] = new_returns_data
        else:
            data.pop('returns', None)

        return data


    def validate_table_number(self, value):
        if value < 0:
            raise ValidationError(_("table-number can not be negative"))
        return value

    def validate_total_price(self, value):
        user = self.context['request'].user
        if value < 0:
            raise ValidationError(_("total-price can not be negative"))
        if user.role in ['waiter', 'reception', 'manager']:
            raise PermissionDenied(_("You do not have the permission to set the bill price"))
        return value

    def validate_bill(self, value):
        user = self.context['request'].user
        if user.branch and value.branch != user.branch:
            raise PermissionDenied(_("You can not create a bill with a different branch"))
        return value

    def validate_items(self, value):
        if self.instance and value:
            raise ValidationError(_("Items cannot be modified when updating a bill."))
        
        if not value:
            raise ValidationError(_("At least one added item must be provided"))

        seen    = set()
        bill_id = self.initial_data.get("bill")
        try:
            bill_obj = models.Bill.objects.get(id=bill_id)
        except models.Bill.DoesNotExist:
            raise ValidationError(_("Invalid bill ID."))

        for data in value:
            branch_product = data["branch_product"]
            if hasattr(branch_product, "branch") and branch_product.branch != bill_obj.branch:
                raise ValidationError(
                    _("{product} does not belong to branch {branch}").format(
                        product=branch_product.name, branch=bill_obj.branch.name
                    )
                )
            if branch_product.id in seen:
                raise ValidationError(_("Duplicate added items detected"))
            seen.add(branch_product.id)

        return value

    def validate_returns(self, value):
        if not self.instance  and  value:  # Create mode
            raise ValidationError(_("Returns are not allowed when creating a new bill."))

        if not value:
            raise ValidationError(_("At least one returned item must be provided"))

        seen     = set()
        bill_obj = self.instance.bill

        for data in value:
            branch_product = data["branch_product"]
            if hasattr(branch_product, "branch") and branch_product.branch != bill_obj.branch:
                raise ValidationError(
                    _("{product} does not belong to bill's branch {branch}").format(
                        product=branch_product.name, branch=bill_obj.branch.name
                    )
                )
            if branch_product.id in seen:
                raise ValidationError(_("Duplicate returned items detected"))
            seen.add(branch_product.id)

        return value


    def process_item(self, obj, quantity, action='add'):
        multiplier     = 1 if action == 'add' else -1
        final_quantity = quantity * multiplier

        if action == 'add' and obj.available_units < quantity:
            raise ValidationError(
                _("{name} has only {available} units").format(
                    name=obj.name, available=obj.available_units
                )
            )
        obj.sold_units += final_quantity
        obj.save()
        for material_data in obj.material_consumptions_set.all():
            material_data.material.available_units -= material_data.consumption * final_quantity
            material_data.material.save()


    def create(self, validated_data):
        validated_data.pop('total_price', None)
        user                         = self.context['request'].user
        validated_data['created_by'] = user
        items_data                   = validated_data.pop('items', [])
        returns_data                 = validated_data.pop('returns', None)
        if returns_data:
            raise ValidationError(_("You cannot return items when creating a bill."))

        with transaction.atomic():
            instance    = super().create(validated_data)
            total_price = 0
            bill_items  = []

            for data in items_data:
                branch_product  = data['branch_product']
                quantity        = data['quantity']
                self.process_item(branch_product, quantity, 'add')
                total_price += branch_product.price * quantity
                bill_items.append(models.CafeBillItem(
                    branch_product = branch_product,
                    quantity       = quantity,
                    notes          = data.get('notes', None)
                ))

            created_items = models.CafeBillItem.objects.bulk_create(bill_items)
            instance.items.add(*created_items)
            instance.total_price = total_price
            instance.save()
            instance.bill.update_products_price()
            return instance


    def update(self, instance, validated_data):
        user         = self.context['request'].user
        items_data   = validated_data.pop('items', [])
        returns_data = validated_data.pop('returns', [])
        total_price  = instance.total_price

        if not instance.bill.is_active and user.role in ['reception', 'waiter']:
            raise PermissionDenied(_("You do not have the permission to edit closed bills"))

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            # Process returns
            for data in returns_data:
                obj               = data['branch_product']
                returned_quantity = data['quantity']
                bill_item = instance.items.filter(branch_product=obj).first()
                if not bill_item or bill_item.quantity < returned_quantity:
                    raise ValidationError(_("Not enough {name} units to return").format(name=obj.name))
                remaining = bill_item.quantity - returned_quantity
                if remaining > 0:
                    bill_item.quantity = remaining
                    bill_item.save()
                else:
                    bill_item.delete()
                self.process_item(obj, returned_quantity, 'return')
                total_price  -= obj.price * returned_quantity
                returned_item = models.CafeBillReturn.objects.create(
                    branch_product = obj,
                    quantity       = returned_quantity,
                    created_by     = user
                )
                instance.returns.add(returned_item)

            # Process additions
            seen = set()
            for data in items_data:
                obj          = data['branch_product']
                add_quantity = data['quantity']
                if obj.id in seen:
                    raise ValidationError(_("Duplicate items detected"))
                seen.add(obj.id)
                self.process_item(obj, add_quantity, 'add')
                total_price += obj.price * add_quantity
                bill_item = instance.items.filter(branch_product=obj).first()
                if bill_item:
                    bill_item.quantity += add_quantity
                    bill_item.save()
                else:
                    bill_item = models.CafeBillItem.objects.create(
                        branch_product = obj,
                        quantity       = add_quantity,
                        notes          = data.get('notes', None)
                    )
                    instance.items.add(bill_item)

            instance.total_price = total_price
            instance.save()
            instance.bill.update_products_price()
            if not instance.bill.is_active:
                instance.bill.update_total_price()
            return instance
