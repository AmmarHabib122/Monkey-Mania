from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from decimal import Decimal
from django.db.models import F  

from base import models
from base.serializers import *








class ProductBillProductSerializer(serializers.ModelSerializer):
    branch_product = serializers.PrimaryKeyRelatedField(
        queryset  = models.BranchProduct.objects.all(),
        required  = True,
        error_messages={
            'does_not_exist': _('You must provide a valid branch product ID.'),
            'incorrect_type': _('Branch product must be identified by an integer ID.')
        }
    )
    options = serializers.PrimaryKeyRelatedField(
        queryset = models.ProductOptions.objects.all(),
        many     = True,
        required = False,
    )
    add_ons = serializers.PrimaryKeyRelatedField(
        queryset = models.ProductAddOns.objects.all(),
        many     = True,
        required = False,
    )

    class Meta:
        model = models.ProductBillProduct
        fields = [
            'id',
            'branch_product',
            'options',
            'add_ons',
            'quantity',
            'unit_price',
            'notes',
            'created',
            'updated',
        ]
        read_only_fields = ['unit_price', 'created', 'updated']

    def to_representation(self, instance):
        data           = super().to_representation(instance)
        branch_product = instance.branch_product
        data['branch_product']    = {'id': branch_product.id, 'name': branch_product.name} if branch_product else None
        data['branch_product_id'] = branch_product.id if branch_product else None
        data['options'] = ProductOptionsSerializer(instance.options.all(), many=True).data
        data['add_ons'] = ProductAddOnsSerializer(instance.add_ons.all(), many=True).data
        return data









class ProductBillReturnedProductSerializer(serializers.ModelSerializer):
    branch_product = serializers.PrimaryKeyRelatedField(
        queryset  = models.BranchProduct.objects.all(),
        required  = True,
        error_messages={
            'does_not_exist': _('You must provide a valid branch product ID.'),
            'incorrect_type': _('Branch product must be identified by an integer ID.')
        }
    )
    options = serializers.PrimaryKeyRelatedField(
        queryset = models.ProductOptions.objects.all(),
        many     = True,
        required = False,
    )
    add_ons = serializers.PrimaryKeyRelatedField(
        queryset = models.ProductAddOns.objects.all(),
        many     = True,
        required = False,
    )

    class Meta:
        model = models.ProductBillReturnedProduct
        fields = [
            'id',
            'branch_product',
            'options',
            'add_ons',
            'quantity',
            'unit_price',
            'created_by',
            'created',
            'updated',
        ]
        read_only_fields = ['unit_price', 'created_by', 'created', 'updated']

    def to_representation(self, instance):
        data           = super().to_representation(instance)
        branch_product = instance.branch_product
        data['branch_product']    = {'id': branch_product.id, 'name': branch_product.name} if branch_product else None
        data['branch_product_id'] = branch_product.id if branch_product else None
        data['options'] = ProductOptionsSerializer(instance.options.all(), many=True).data
        data['add_ons'] = ProductAddOnsSerializer(instance.add_ons.all(), many=True).data
        return data













class ProductBillSerializer(serializers.ModelSerializer):
    products            = ProductBillProductSerializer(many = True, required = True)
    returned_products   = ProductBillReturnedProductSerializer(many = True, required = False)
    bill                = serializers.PrimaryKeyRelatedField(
        queryset = models.Bill.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid bill ID.'),
            'does_not_exist': _('You must provide a valid bill ID.'),
            'incorrect_type': _('bill must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.ProductBill
        fields = [
            'id',
            'bill_number',
            'table_number',
            'total_price',
            'take_away',
            'bill',
            'products',
            'returned_products',
            'notes',
            'created_by',
            'created',
            'updated',
        ]
        read_only_fields = [
            'bill_number',
            'total_price',
            'created_by',
            'created',
            'updated',
        ]
        
        
  

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        created_by = instance.created_by
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        bill = instance.bill
        data['first_child'] = bill.children.all().first().name if bill.children.exists() else None
        data['branch'] = bill.branch.name if bill.branch else None
        data['branch_id'] = bill.branch.id if bill.branch else None
        # Process products
        new_products_data = []
        for product_data in data.get('products', []):
            product = product_data.get('product', {})
            if product:
                product_type = product.get('type', 'product')
                new_products_data.append({
                    'id': product.get('id', None),
                    'unit_price': product.get('price', 0),
                    'total_price': float(product.get('price', 0)) * float(product_data['quantity']),
                    'quantity': product_data['quantity'],
                    'notes': product_data['notes'],
                    'name': product.get('name', 'Unknown Product'),
                })
        data['products'] = new_products_data

        # Process returned products if allowed
        if request and request.user.role not in ['waiter', 'reception']:
            new_returned_products_data = []
            for returned_data in data.get('returned_products', []):
                product = returned_data.get('product', {})
                if product:
                    product_type = product.get('type', 'product')
                    created_by_user = models.User.objects.filter(id = returned_data['created_by']).first()
                    new_returned_products_data.append({
                        'id': product.get('id', None),
                        'name': product.get('name', 'Unknown Product'),
                        'quantity': returned_data['quantity'],
                        'created_by' : created_by_user.username if created_by_user else None,
                        'created_by_id' : created_by_user.id if created_by_user else None,
                    })
            data['returned_products'] = new_returned_products_data
        else:
            data.pop('returned_products', None)

        # Clean up empty values
        data['products'] = [p for p in data.get('products', []) if p]
        return data





    def validate_table_number(self, value):
        if value < 0: 
            raise ValidationError(_("table-number can not be negative"))
        return value

    def validate_total_price(self, value):
        user = self.context['request'].user
        if value < 0: 
            raise ValidationError(_("total-price can not be negative"))
        if user.role in ['waiter', 'reception']:
            raise PermissionDenied(_("You do not have the permission to set the bill price"))
        return value

    def validate_bill(self, value):
        user = self.context['request'].user
        if user.branch   and   value.branch != user.branch:
            raise PermissionDenied(_("You can not create a bill with a different branch"))
        return value
    
    def validate_products(self, value):
        if not self.instance:  # 🚨 Create mode
            if not value:
                raise ValidationError(_("At least one added item must be provided"))

            seen = set()
            bill_id = self.initial_data.get("bill")

            try:
                bill_obj = models.Bill.objects.get(id=bill_id)
            except models.Bill.DoesNotExist:
                raise ValidationError(_("Invalid bill ID."))

            for data in value:
                if "product_object" not in data:
                    raise ValidationError(_("Invalid item data"))

                obj = data["product_object"]

                # 🚨 Branch check
                if hasattr(obj, "branch") and obj.branch != bill_obj.branch:
                    raise ValidationError(
                        _("{product} does not belong to branch {branch}").format(
                            product=obj.name, branch=bill_obj.branch.name
                        )
                    )

                key = (ContentType.objects.get_for_model(obj).id, obj.id)
                if key in seen:
                    raise ValidationError(_("Duplicate added items detected"))
                seen.add(key)

        else:  # 🚨 Update mode
            if value:
                raise ValidationError(_("Products cannot be modified when updating a bill."))

        return value

    
    
    def validate_returned_products(self, value):
        # 🚨 On CREATE → must be empty
        if not self.instance:  # create mode
            if value:
                raise ValidationError(_("Returned products are not allowed when creating a new bill."))
            return value  # just return, no validation needed

        # 🚨 On UPDATE → must have at least one item
        if not value:
            raise ValidationError(_("At least one returned item must be provided"))

        seen = set()
        bill_obj = self.instance.bill  # always from instance in update

        for data in value:
            if "product_object" not in data:
                raise ValidationError(_("Invalid item data"))

            obj = data["product_object"]

            # Branch check
            if hasattr(obj, "branch") and obj.branch != bill_obj.branch:
                raise ValidationError(
                    _("{product} does not belong to bill's branch {branch}").format(
                        product=obj.name, branch=bill_obj.branch.name
                    )
                )

            key = (ContentType.objects.get_for_model(obj).id, obj.id)
            if key in seen:
                raise ValidationError(_("Duplicate returned items detected"))
            seen.add(key)

        return value

        


 
    def process_item(self, obj, quantity, action='add'):
        """Unified method to process products/offers for add/return"""
        multiplier     = 1 if action == 'add' else -1
        final_quantity = quantity * multiplier

        if isinstance(obj, models.BranchProduct):
            # Process individual product
            if action == 'add' and obj.available_units < quantity:
                raise ValidationError(
                    _("{name} has only {available} units").format(
                        name      = obj.name, 
                        available = obj.available_units
                    )
                )
            obj.sold_units += final_quantity
            obj.save()
            # Update materials
            for material_data in obj.material_consumptions_set.all():
                material_data.material.available_units -= material_data.consumption * final_quantity
                material_data.material.save()


        elif isinstance(obj, models.BranchOffer):
            # Process offer and its components
            if action == 'add':
                for product_data in obj.products_set.select_related('product'):
                    if product_data.product.available_units < (product_data.quantity * quantity):
                        raise ValidationError(
                            _("{product} in offer {offer} has only {available} units available").format(
                                product   = product_data.product.name,
                                offer     = obj.name,
                                available = product_data.product.available_units
                            )
                        )
            obj.sold_units += final_quantity
            obj.save()
            # Process contained products
            for product_data in obj.products_set.select_related('product'):
                product             = product_data.product
                final_quantity      = product_data.quantity * final_quantity
                product.sold_units += final_quantity
                product.save()
                # Update materials
                for material_data in product.material_consumptions_set.all():
                    material_data.material.available_units -= material_data.consumption * final_quantity
                    material_data.material.save()







    def create(self, validated_data):
        validated_data.pop('total_price', None)
        user                         = self.context['request'].user
        validated_data['created_by'] = user
        products_data                = validated_data.pop('products', [])
        returned_products_data       = validated_data.pop('returned_products', None)
        # Check for returned_products in the input data
        if returned_products_data:
            raise ValidationError(_("You cannot return items when creating a bill."))


        with transaction.atomic():
            instance      = super().create(validated_data)
            total_price   = 0
            bill_products = []

            for data in products_data:
                obj      = data['product_object']
                quantity = data['quantity']
                # Validate and process
                self.process_item(obj, quantity, 'add')
                total_price += obj.price * quantity
                # Create bill product record
                bill_products.append(models.ProductBillProduct(
                    product_type = ContentType.objects.get_for_model(obj),
                    product_id   = obj.id,
                    quantity     = quantity,
                    notes        = data.get('notes', None)
                ))

            created_products = models.ProductBillProduct.objects.bulk_create(bill_products)
            instance.products.add(*created_products)
            instance.total_price = total_price
            instance.save()
            instance.bill.update_products_price()
            return instance







    def update(self, instance, validated_data):
        user                   = self.context['request'].user
        products_data          = validated_data.pop('products', [])
        returned_products_data = validated_data.pop('returned_products', [])
        total_price            = instance.total_price

        if not instance.bill.is_active  and  user.role in ['reception', 'waiter']:
            raise PermissionDenied(_("You do not have the permissio to edit closed bills"))

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            # Process returns
            for data in returned_products_data:
                obj               = data['product_object']
                returned_quantity = data['quantity']
                # Find existing item
                bill_item = instance.products.filter(
                    product_type = ContentType.objects.get_for_model(obj),
                    product_id   = obj.id
                ).first()
                if not bill_item or bill_item.quantity < returned_quantity:
                    raise ValidationError(_("Not enough {name} units to return").format(name=obj.name))
                # Update quantities
                remaining = bill_item.quantity - returned_quantity
                if remaining > 0:
                    bill_item.quantity = remaining
                    bill_item.save()
                else:
                    bill_item.delete()
                # Reverse operations
                self.process_item(obj, returned_quantity, 'return')
                total_price -= obj.price * returned_quantity
                # Create return record
                returned_item  = models.ProductBillReturnedProduct.objects.create(
                    product_type  = ContentType.objects.get_for_model(obj),
                    product_id    = obj.id,
                    quantity      = returned_quantity,
                    created_by    = user
                )
                instance.returned_products.add(returned_item)



            # Process additions/updates
            seen = set()
            for data in products_data:
                obj          = data['product_object']
                add_quantity = data['quantity']
                # Check duplicates
                key = (ContentType.objects.get_for_model(obj).id, obj.id)
                if key in seen:
                    raise ValidationError(_("Duplicate items detected"))
                seen.add(key)
                # Process addition
                self.process_item(obj, add_quantity, 'add')
                total_price += obj.price * add_quantity
                # Check if the product already exists in the bill
                bill_item = models.ProductBillProduct.objects.filter(
                    product_type = ContentType.objects.get_for_model(obj),
                    product_id   = obj.id
                ).first()

                if bill_item:
                    # Update existing item
                    bill_item.quantity += add_quantity
                    bill_item.save()
                else:
                    # Create new item
                    bill_item = models.ProductBillProduct.objects.create(
                        product_type = ContentType.objects.get_for_model(obj),
                        product_id   = obj.id,
                        quantity     = add_quantity,
                        notes        = data.get('notes', None)
                    )
                    instance.products.add(bill_item)

            # Finalize
            instance.total_price = total_price
            instance.save()
            instance.bill.update_products_price()
            if not instance.bill.is_active:
                instance.bill.update_total_price()
            return instance


         




