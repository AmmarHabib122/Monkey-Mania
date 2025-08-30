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
    product_type = serializers.CharField(write_only=True)
    product_id   = serializers.IntegerField(write_only=True)
    product      = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ProductBillProduct
        fields = [
            'id',
            'product_type',
            'product_id',
            'product',
            'quantity',
            'notes'
        ]

    

    def validate(self, attrs):
        content_type_map = {
            'product': 'branchproduct',
            'offer': 'branchoffer'
        }
        product_type = attrs['product_type'].lower()
        if product_type not in content_type_map:
            raise ValidationError(
                _("Invalid product type. Allowed values: product, offer.")
            )
        try:
            model_type = content_type_map[attrs['product_type'].lower()]
            content_type = ContentType.objects.get(model=model_type)
            obj = content_type.get_object_for_this_type(id=attrs['product_id'])
        except (KeyError, ContentType.DoesNotExist, ObjectDoesNotExist):
            raise ValidationError(_("Invalid product type or ID"))

        attrs['product_object'] = obj
        attrs['product_type'] = content_type
        attrs['product_id'] = attrs['product_id']
        return attrs
    

    
    def get_product(self, obj):
        if isinstance(obj.product_object, models.BranchProduct):
            data = BranchProductSerializer(obj.product_object).data
            data['type'] = 'product'
            return data
        elif isinstance(obj.product_object, models.BranchOffer):
            data = BranchOfferSerializer(obj.product_object).data
            data['type'] = 'offer'
            return data
        return None









class ProductBillReturnedProductSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ProductBillReturnedProduct
        fields = [
            'id',
            'product_type',
            'product_id',
            'product',
            'quantity',
            'created_by'
        ]
        read_only_fields = ['created_by']

    

    def validate(self, attrs):
        content_type_map = {
            'product': 'branchproduct',
            'offer': 'branchoffer'
        }
        product_type = attrs['product_type'].lower()
        if product_type not in content_type_map:
            raise ValidationError(
                _("Invalid product type. Allowed values: product, offer.")
            )
        try:
            model_type = content_type_map[attrs['product_type'].lower()]
            content_type = ContentType.objects.get(model=model_type)
            obj = content_type.get_object_for_this_type(id=attrs['product_id'])
        except (KeyError, ContentType.DoesNotExist, ObjectDoesNotExist):
            raise ValidationError(_("Invalid product type or ID"))

        attrs['product_object'] = obj
        attrs['product_type'] = content_type
        attrs['product_id'] = attrs['product_id']
        return attrs

    def get_product(self, obj):
        if isinstance(obj.product_object, models.BranchProduct):
            data = BranchProductSerializer(obj.product_object).data
            data['type'] = 'product'
            return data
        elif isinstance(obj.product_object, models.BranchOffer):
            data = BranchOfferSerializer(obj.product_object).data
            data['type'] = 'offer'
            return data
        return None













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
                    new_returned_products_data.append({
                        'name': product.get('name', 'Unknown Product'),
                        'quantity': returned_data['quantity'],
                        'created_by' : returned_data['created_by']
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
        if not value:
            raise ValidationError(_("At least one added item must be provided"))

        seen = set()
        bill = self.initial_data.get("bill")  # bill ID from request

        try:
            bill_obj = models.Bill.objects.get(id=bill)
        except models.Bill.DoesNotExist:
            raise ValidationError(_("Invalid bill ID."))

        for data in value:
            if 'product_object' not in data:
                raise ValidationError(_("Invalid item data"))
            obj = data['product_object']

            # 🚨 Branch check here
            if hasattr(obj, "branch") and obj.branch != bill_obj.branch:
                raise ValidationError(
                    _("{product} does not belong to bill's branch {branch}").format(
                        product=obj.name, branch=bill_obj.branch.name
                    )
                )

            key = (ContentType.objects.get_for_model(obj).id, obj.id)
            if key in seen:
                raise ValidationError(_("Duplicate added items detected"))
            seen.add(key)
        return value
    
    
def validate_returned_products(self, value):
    if not value:
        raise ValidationError(_("At least one returned item must be provided"))

    seen = set()
    bill = self.initial_data.get("bill")

    try:
        bill_obj = models.Bill.objects.get(id=bill)
    except models.Bill.DoesNotExist:
        raise ValidationError(_("Invalid bill ID."))

    for data in value:
        if 'product_object' not in data:
            raise ValidationError(_("Invalid item data"))
        obj = data['product_object']

        # 🚨 Branch check here
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

        if not instance.bill.is_active:
            raise PermissionDenied(_("Cannot edit closed bills"))

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
            return instance


        







   

    '''my first methods withour including the offers'''
    # def create(self, validated_data):
    #     validated_data.pop('total_price', None)
    #     user                               = self.context['request'].user
    #     validated_data['created_by']       = user
    #     products                           = validated_data.pop('products', None)

    #     with transaction.atomic():
    #         instance             = super().create(validated_data)
    #         total_price          = 0
    #         new_bill_products    = []

    #         for data in products:
    #             product  = data['product_object']
    #             quantity = data['quantity']

    #             if product.available_units < quantity:
    #                 raise ValidationError(_("{name} available units are less than the quantity you entered").format(name = product.name))
    #             else:
    #                 new_bill_products.append(
    #                     models.ProductBillProduct(
    #                         product_bill = instance,
    #                         product      = product,
    #                         quantity     = quantity,
    #                     )
    #                 )
    #                 '''substracting the material used in manifacturing the product'''
    #                 for data in product.material_consumptions_set.all():
    #                     product_material_consumption = data.consumption 
    #                     material                     = data.material
    #                     material.available_units    -= product_material_consumption
    #                     material.save()

    #                 total_price        += product.price * quantity
    #                 product.sold_units += quantity
    #                 product.save()
    #         models.ProductBillProduct.objects.bulk_create(new_bill_products)
    #         instance.total_price = total_price
    #         instance.bill.update_products_price()            #update the child bill price to reflect product bill price changes
    #         instance.save()
    #         return instance
    


    # def update(self, instance, validated_data):
    #     user                               = self.context['request'].user
    #     products                           = validated_data.pop('products', [])
    #     returned_products                  = validated_data.pop('returned_products', [])
    #     request_total_price                = validated_data.pop('total_price', None)
    #     total_price                        = instance.total_price

    #     if user.role in ['reception', 'waiter']:
    #         if instance.bill.is_active == False:
    #             raise PermissionDenied(_("You can not edit this bill anymore"))

    #     with transaction.atomic():
    #         instance = super().update(instance, validated_data)
    #         if returned_products != []:
    #             new_bill_returned_products = []

    #             for data in returned_products:
    #                 product          = data['product_object']
    #                 quantity         = data['quantity']
    #                 instance_product = instance.products.filter(product = product).first()
    #                 if    not instance_product    or    instance_product.quantity < quantity:
    #                     raise ValidationError(_("{name} units in the bill is less than the desired returned units").format(name = product.name))
    #                 else:
    #                     if instance_product.quantity > quantity:
    #                         products.append({            #ex: the user tried to return just one-item-quntity  from the item qunaitity so we return the whole and add one again in the produts
    #                             "product"  : data['product_object'],
    #                             "quantity" : instance_product.quantity - quantity,
    #                         })
    #                         total_price        -= product.price * (instance_product.quantity - quantity)
    #                         product.sold_units -= instance_product.quantity - quantity
    #                     instance_product.delete()
    #                     new_bill_returned_products.append(
    #                         models.ProductBillReturnedProduct(
    #                             product_bill = instance,
    #                             product      = product,
    #                             quantity     = quantity,
    #                             created_by   = user,
    #                         )
    #                     )
                        
    #                     '''adding the material substracted in creating the products for the bill cause the product is not manifactured yet'''
    #                     for data in product.material_consumptions_set.all():
    #                         product_material_consumption = data.consumption 
    #                         material                     = data.material
    #                         material.available_units    += quantity * product_material_consumption
    #                         material.save()

    #                     total_price        -= product.price * quantity
    #                     product.sold_units -= quantity
    #                     product.save()
            
    #             models.ProductBillReturnedProduct.objects.bulk_create(new_bill_returned_products)

    #         if products != []:
    #             products_check    = [data['product_object'].id for data in products]
    #             if len(products_check) != len(set(products_check)):
    #                 raise ValidationError(_("You tried to add and return the same product at the same time"))
                
    #             new_bill_products = []
    #             for data in products:
    #                 product  = data['product_object']
    #                 quantity = data['quantity']
    #                 already_existing_product = instance.products.all().filter(id = product.id).first()


    #                 if product.available_units < quantity:
    #                     raise ValidationError(_("{name} available units are less than the quantity you entered").format(name = product.name))
    #                 elif already_existing_product:
    #                     already_existing_product.quantity    += quantity
    #                     total_price                          += already_existing_product.product.price * quantity
    #                     already_existing_product.save()
    #                 else:
    #                     new_bill_products.append(
    #                         models.ProductBillProduct(
    #                             product_bill = instance,
    #                             product      = product,
    #                             quantity     = quantity,
    #                         )
    #                     )
    #                     '''substracting the material used in manifacturing the product'''
    #                     for data in product.material_consumptions_set.all():
    #                         product_material_consumption = data.consumption 
    #                         material                     = data.material
    #                         material.available_units    -= quantity * product_material_consumption
    #                         material.save()

    #                     total_price        += product.price * quantity
    #                     product.sold_units += quantity
    #                     product.save()
    #             models.ProductBillProduct.objects.bulk_create(new_bill_products)

    #         instance.total_price = request_total_price if request_total_price else total_price
    #         instance.bill.update_products_price()         #update the child bill price to reflect product bill price changes
    #         instance.save()
    #         return instance
                
        

  # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     data    = super().to_representation(instance)

    #     for product_data in data.get('products', []):
    #         product  = product_data['product']
    #         product  = models.BranchProduct.objects.filter(id = product_data['product']).first()
    #         for product_data in data['products']:
    #             product = product_data['product']
    #             product_data.update({
    #                 'unit_price': product.get('price', 0),
    #                 'total_price': product.get('price', 0) * product_data['quantity'],
    #                 'type': 'offer' if 'BranchOffer' in str(product) else 'product'
    #             })
            
    #     if request.user.role not in ['waiter', 'reception']:
    #         data.pop('returned_products', None)
    #     else:
    #         for product_data in data.get('returned_products', []):
    #             product = models.BranchProduct.objects.filter(id = product_data['product']).first()
    #             if product:
    #                 product  = product_data['product']
    #                 product_data['name']  = product.name

    #     return data










# class ProductBillProductSerializer(serializers.ModelSerializer):
#     product   = serializers.PrimaryKeyRelatedField(
#         queryset = models.BranchProduct.objects.all(), 
#         required = True,
#         error_messages={
#             'invalid': _('Invalid product ID.'),
#             'does_not_exist': _('You must provide a valid product ID.'),
#             'incorrect_type': _('product must be identified by an integer ID.')
#         }
#     ) 
#     class Meta:
#         model = models.ProductBillProduct
#         fields = [
#             'id',
#             'product',
#             'quantity',
#             'notes',
#         ]
#     def validate_quantity(self, value):
#         if value <= 0: 
#             raise ValidationError(_("Quantity can not be negative or equal to zero"))
#         return value
    




# class ProductBillReturnedProductSerializer(serializers.ModelSerializer):
#     product   = serializers.PrimaryKeyRelatedField(
#         queryset = models.BranchProduct.objects.all(), 
#         required = True,
#         error_messages={
#             'invalid': _('Invalid product ID.'),
#             'does_not_exist': _('You must provide a valid product ID.'),
#             'incorrect_type': _('product must be identified by an integer ID.')
#         }
#     ) 
#     class Meta:
#         model = models.ProductBillReturnedProduct
#         fields = [
#             'id',
#             'product',
#             'quantity',
#             'created_by'
#         ]
#         read_only_fields = [
#             'created_by',
#         ]
#     def validate_quantity(self, value):
#         if value <= 0: 
#             raise ValidationError(_("Quantity can not be negative or equal to zero"))
#         return value
    
#     def create(self, validated_data):
#         user                           = self.context['request'].user
#         validated_data['created_by']   = user
#         return super().create(validated_data)

