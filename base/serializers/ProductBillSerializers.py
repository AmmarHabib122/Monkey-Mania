from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.utils.translation import gettext as _

from base import models
from base.serializers.ProductSerializers import ProductOptionsSerializer, ProductAddOnsSerializer
from base.services.ProductBillService import ProductBillService




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
        model  = models.ProductBillProduct
        fields = ['id', 'branch_product', 'options', 'add_ons', 'quantity', 'unit_price', 'notes', 'created', 'updated']
        read_only_fields = ['unit_price', 'created', 'updated']

    def to_representation(self, instance):
        data           = super().to_representation(instance)
        branch_product = instance.branch_product
        data['branch_product']    = {'id': branch_product.id, 'name': branch_product.name} if branch_product else None
        data['branch_product_id'] = branch_product.id if branch_product else None
        data['options']           = ProductOptionsSerializer(instance.options.all(), many=True).data
        data['add_ons']           = ProductAddOnsSerializer(instance.add_ons.all(), many=True).data
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
        model  = models.ProductBillReturnedProduct
        fields = ['id', 'branch_product', 'options', 'add_ons', 'quantity', 'unit_price', 'created_by', 'created', 'updated']
        read_only_fields = ['unit_price', 'created_by', 'created', 'updated']

    def to_representation(self, instance):
        data           = super().to_representation(instance)
        branch_product = instance.branch_product
        created_by     = instance.created_by
        data['branch_product']    = {'id': branch_product.id, 'name': branch_product.name} if branch_product else None
        data['branch_product_id'] = branch_product.id if branch_product else None
        data['created_by']        = created_by.username if created_by else None
        data['created_by_id']     = created_by.id if created_by else None
        data['options']           = ProductOptionsSerializer(instance.options.all(), many=True).data
        data['add_ons']           = ProductAddOnsSerializer(instance.add_ons.all(), many=True).data
        return data




class ProductBillSerializer(serializers.ModelSerializer):
    products          = ProductBillProductSerializer(many=True, required=True)
    returned_products = ProductBillReturnedProductSerializer(many=True, required=False)
    bill              = serializers.PrimaryKeyRelatedField(
        queryset = models.Bill.objects.all(),
        required = True,
        error_messages={
            'invalid': _('Invalid bill ID.'),
            'does_not_exist': _('You must provide a valid bill ID.'),
            'incorrect_type': _('bill must be identified by an integer ID.')
        }
    )

    class Meta:
        model  = models.ProductBill
        fields = [
            'id', 'bill_number', 'table_number', 'total_price', 'take_away',
            'bill', 'products', 'returned_products', 'notes',
            'created_by', 'created', 'updated',
        ]
        read_only_fields = ['bill_number', 'total_price', 'created_by', 'created', 'updated']

    def to_representation(self, instance):
        data       = super().to_representation(instance)
        created_by = instance.created_by
        bill       = instance.bill
        data['created_by']    = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        data['first_child']   = bill.children.first().name if bill.children.exists() else None
        data['branch']        = bill.branch.name if bill.branch else None
        data['branch_id']     = bill.branch.id if bill.branch else None
        request = self.context.get('request')
        if not request or request.user.role in ['waiter', 'reception']:
            data.pop('returned_products', None)
        return data


    # ──────────────────────────────────────────────
    # Validators
    # ──────────────────────────────────────────────

    def validate_bill(self, value):
        user = self.context['request'].user
        if user.branch and value.branch != user.branch:
            raise PermissionDenied(_("You can not create a bill with a different branch"))
        return value

    def validate_table_number(self, value):
        if value < 0:
            raise ValidationError(_("table-number can not be negative"))
        return value

    def validate_products(self, value):
        if not self.instance:
            if not value:
                raise ValidationError(_("At least one product must be provided"))
        else:
            raise ValidationError(_("You cannot add products to an existing bill. please create a new one for the new products."))

        bill = models.Bill.objects.filter(id=self.initial_data.get('bill')).first()
        
        seen = set()
        for data in value:
            branch_product = data['branch_product']
            if branch_product.branch != bill.branch:
                raise ValidationError(
                    _("{product} does not belong to branch {branch}").format(
                        product=branch_product.name, branch=bill.branch.name
                    )
                )
            if branch_product.id in seen:
                raise ValidationError(_("Duplicate products detected"))
            seen.add(branch_product.id)
        return value



    def validate_returned_products(self, value):
        if not self.instance:
            if value:
                raise ValidationError(_("Returned products are not allowed when creating a new bill."))

        if not value:
            return value

        seen = set()
        for data in value:
            branch_product = data['branch_product']
            if branch_product.branch != self.instance.bill.branch:
                raise ValidationError(
                    _("{product} does not belong to bill's branch {branch}").format(
                        product=branch_product.name, branch=self.instance.bill.branch.name
                    )
                )
            if branch_product.id in seen:
                raise ValidationError(_("Duplicate returned items detected"))
            seen.add(branch_product.id)

            product_bill_product = self.instance.products.filter(branch_product=branch_product).first()
            if not product_bill_product or product_bill_product.quantity < data['quantity']:
                raise ValidationError(
                    _("There is no enough units of the product {name} to be returned").format(name=branch_product.name)
                )
        return value


    # ──────────────────────────────────────────────
    # Create / Update
    # ──────────────────────────────────────────────

    def create(self, validated_data):
        user          = self.context['request'].user
        products_data = validated_data.pop('products', [])
        validated_data.pop('returned_products', None)
        validated_data['created_by'] = user

        with transaction.atomic():
            instance             = super().create(validated_data)
            instance.total_price = sum(
                (ProductBillService.add_product(instance, data, user) for data in products_data),
                Decimal('0')
            )
            instance.save()
            instance.bill.update_products_price()
            return instance




    def update(self, instance, validated_data):
        user                   = self.context['request'].user
        products_data          = validated_data.pop('products', [])
        returned_products_data = validated_data.pop('returned_products', [])

        if not instance.bill.is_active and user.role in ['reception', 'waiter']:
            raise PermissionDenied(_("You do not have the permission to edit closed bills"))

        with transaction.atomic():
            instance    = super().update(instance, validated_data)
            total_price = instance.total_price

            for data in returned_products_data:
                total_price -= ProductBillService.return_product(instance, data, user)
            

            instance.total_price = total_price
            instance.save()
            instance.bill.update_products_price()
            if not instance.bill.is_active:
                instance.bill.update_total_price()
            return instance
