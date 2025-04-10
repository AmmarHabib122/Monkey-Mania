from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from base import models
from base import libs






'''##############################OfferSrializers######################################'''

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = [
            'id',
            'name',
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]

    def validate_name(self, value):
        return value.lower()
    
    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)
    






'''##############################BranchOfferSerializers######################################'''

class BranchOfferProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=models.BranchProduct.objects.all(),
        required=True,
        error_messages={
            'invalid': _('Invalid product ID.'),
            'does_not_exist': _('You must provide a valid product ID.'),
            'incorrect_type': _('Product must be identified by an integer ID.')
        }
    )

    class Meta:
        model = models.BranchOfferProduct
        fields = [
            'id',
            'product',
            'quantity',
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError(_("Quantity cannot be less than one"))
        return value
    




class BranchOfferSerializer(serializers.ModelSerializer):
    products_set = BranchOfferProductSerializer(many=True, required=True)

    offer = serializers.PrimaryKeyRelatedField(
        queryset = models.Offer.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid offer ID.'),
            'does_not_exist': _('You must provide a valid offer ID.'),
            'incorrect_type': _('offer must be identified by an integer ID.')
        }
    ) 
    branch  = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    
    class Meta:
        model = models.BranchOffer
        fields = [
            'id',
            'name',
            'offer',
            'branch',
            'products_set',
            'price',
            'before_sale_price',
            'sold_units',
            'expire_date',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'name',
            'before_sale_price',
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]

    def validate_price(self, value):
        if value < 0: 
            raise ValidationError(_("Offer Price can not be negative."))
        return value
    
    def validate_expire_date(self, value):
        if value <= timezone.now().date():
            raise ValidationError(_("Expire date must be in the future"))
        return value
    
    def validate_branch(self, value):
        user  = self.context['request'].user
        if    user.branch    and    value != user.branch:
            raise PermissionDenied(_("You can not add an offer to this branch"))
        return value
    
    def validate_products_set(self, value):
        if not value:
            raise ValidationError(_("At least one product must be provided."))
        product_ids = [item['product'].id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise ValidationError(_("Duplicate products are not allowed."))
        return value

    def create(self, validated_data):
        user                         = self.context['request'].user
        products_data                = validated_data.pop('products_set')
        validated_data['created_by'] = user

        with transaction.atomic():
            instance = super().create(validated_data)
            products = [
                models.BranchOfferProduct(
                    offer     = instance,
                    product   = product_data['product'],
                    quantity  = product_data['quantity']
                )
                for product_data in products_data
            ]
            models.BranchOfferProduct.objects.bulk_create(products)
        return instance
        
    





    def update(self, instance, validated_data):
        products_data = validated_data.pop('products_set', None)
        
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if products_data is not None:
                # Delete existing products and recreate
                instance.products_set.all().delete()
                products = [
                    models.BranchOfferProduct(
                        offer    = instance,
                        product  = product_data['product'],
                        quantity = product_data['quantity']
                    )
                    for product_data in products_data
                ]
                models.BranchOfferProduct.objects.bulk_create(products)
        instance.save()
        return instance
    




