from django.db import models
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType




class ProductBill(models.Model):
    bill_number        = models.IntegerField(editable=False)
    table_number       = models.IntegerField()
    take_away          = models.BooleanField()
    bill               = models.ForeignKey('base.Bill', on_delete = models.CASCADE, related_name = 'product_bills_set')
    total_price        = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    products           = models.ManyToManyField('base.ProductBillProduct')
    returned_products  = models.ManyToManyField('base.ProductBillReturnedProduct')
    created_by         = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_bills_set')
    created            = models.DateTimeField(auto_now_add = True)
    updated            = models.DateTimeField(auto_now = True)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        if not self.bill_number:
            last_order = ProductBill.objects.filter(bill__branch=self.bill.branch).order_by('-bill_number').first()
            self.bill_number = (last_order.bill_number + 1) if last_order else 1
        super().save(force_insert, force_update, using, update_fields)
        
    def __str__(self):
        bill = self.bill if self.bill else None
        child = self.bill.children.first() if bill else None
        return f"#{self.id} {child.name}" if child else f"#{self.id}"







class ProductBillProduct(models.Model):
    product_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    product_id     = models.PositiveIntegerField()
    product_object = fields.GenericForeignKey('product_type', 'product_id')
    quantity       = models.IntegerField()
    notes          = models.CharField(max_length = 75, null = True)
    created         = models.DateTimeField(auto_now_add = True)
    updated         = models.DateTimeField(auto_now = True)








class ProductBillReturnedProduct(models.Model):
    product_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    product_id     = models.PositiveIntegerField()
    product_object = fields.GenericForeignKey('product_type', 'product_id')
    quantity       = models.IntegerField()
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_bill_returned_products_set')
    created         = models.DateTimeField(auto_now_add = True)
    updated         = models.DateTimeField(auto_now = True)




















# class ProductBillProduct(models.Model):
#     product_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, related_name = 'products_set')
#     product      = models.ForeignKey('base.BranchProduct', on_delete = models.PROTECT)
#     quantity     = models.IntegerField()
#     notes        = models.CharField(max_length = 75, null = True)








# class ProductBillReturnedProduct(models.Model):
#     product_bill = models.ForeignKey('base.ProductBill', on_delete = models.CASCADE, related_name = 'returned_products_set')
#     product      = models.ForeignKey('base.BranchProduct', on_delete = models.PROTECT)
#     quantity     = models.IntegerField()
#     created_by   = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_returned_products_set')


