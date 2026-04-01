from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, PermissionDenied

from base import models


class ProductBillService:

    @staticmethod
    def create_material_transactions(branch_product, options, add_ons, quantity, source_obj, user, action):
        """
        Bulk-create MaterialTransaction records and update BranchMaterial.available_units.
        action: 'stock_out' (adding) | 'stock_in' (returning)
        """
        branch      = branch_product.branch
        source_type = ContentType.objects.get_for_model(source_obj)
        is_out      = action == 'stock_out'

        transactions        = []

        def queue(material, consumed):
            branch_material = models.BranchMaterial.objects.filter(material=material, branch=branch).first()

            if not branch_material:
                raise ValidationError(f"{material.name} is not available in branch {branch.name}")
            
            transactions.append(models.MaterialTransaction(
                branch_material  = branch_material,
                branch           = branch,
                quantity         = consumed,
                transaction_type = action,
                source_type      = source_type,
                source_id        = source_obj.id,
                created_by       = user,
            ))
            branch_material.available_units = branch_material.available_units - consumed if is_out else branch_material.available_units + consumed
            branch_material.save(update_fields=['available_units'])

        for recipe in branch_product.product.reciepe_set.select_related('material').all():
            queue(recipe.material, recipe.consumption * quantity)
        for option in options:
            queue(option.material, option.consumption * quantity)
        for add_on in add_ons:
            queue(add_on.material, add_on.consumption * quantity)

        models.MaterialTransaction.objects.bulk_create(transactions)
        

    @staticmethod
    def add_product(product_bill, data, user):
        """Add a product to a bill (merges if already present). Returns the added total."""
        branch_product = data['branch_product']
        options        = data.get('options', [])
        add_ons        = data.get('add_ons', [])
        quantity       = data['quantity']

        unit_price   = branch_product.product.price
        product_bill_product = models.ProductBillProduct.objects.create(
            product_type   = ContentType.objects.get_for_model(branch_product),
            product_id     = branch_product.id,
            branch_product = branch_product,
            quantity       = quantity,
            unit_price     = unit_price,
            notes          = data.get('notes'),
        )
        if options:
            product_bill_product.options.set(options)
        if add_ons:
            product_bill_product.add_ons.set(add_ons)
        ProductBillService.create_material_transactions(
            branch_product, options, add_ons, quantity, product_bill_product, user, 'stock_out'
        )
        product_bill.products.add(product_bill_product)
        product_bill.save()

        return unit_price * quantity




    @staticmethod
    def return_product(product_bill, data, user):
        """Return a product from a bill. Returns the returned total."""
        branch_product      = data['branch_product']
        options             = data.get('options', [])
        add_ons             = data.get('add_ons', [])
        returned_quantity   = data['quantity']

        product_bill_product    = product_bill.products.filter(branch_product=branch_product).first()
        unit_price      = product_bill_product.unit_price 

        remaining_quantity = product_bill_product.quantity - returned_quantity
        if remaining_quantity > 0:
            product_bill_product.quantity = remaining_quantity
            product_bill_product.save()
        else:
            product_bill_product.delete()

        returned_item = models.ProductBillReturnedProduct.objects.create(
            product_type   = ContentType.objects.get_for_model(branch_product),
            product_id     = branch_product.id,
            branch_product = branch_product,
            quantity       = returned_quantity,
            unit_price     = unit_price,
            created_by     = user,
        )
        returned_item.options.set(product_bill_product.options.all())
        returned_item.add_ons.set(product_bill_product.add_ons.all())
        product_bill.returned_products.add(returned_item)

        ProductBillService.create_material_transactions(
            branch_product, options, add_ons, returned_quantity, returned_item, user, 'stock_in'
        )
        return unit_price * returned_quantity
