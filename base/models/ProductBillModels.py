from django.db import models
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType

from django.utils import timezone
from datetime import timedelta
import random



class ProductBill(models.Model):
    bill_number        = models.IntegerField(editable=False)
    table_number       = models.IntegerField()
    take_away          = models.BooleanField()
    bill               = models.ForeignKey('base.Bill', on_delete = models.CASCADE, related_name = 'product_bills_set')
    total_price        = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    products           = models.ManyToManyField('base.ProductBillProduct')
    returned_products  = models.ManyToManyField('base.ProductBillReturnedProduct')
    notes              = models.CharField(max_length = 75, null = True)
    created_by         = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_bills_set')
    created            = models.DateTimeField(auto_now_add = True)
    updated            = models.DateTimeField(auto_now = True)

    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        last_bill           = ProductBill.objects.filter(bill__branch=self.bill.branch).order_by('-bill_number').first()
        current_time        = timezone.now()
        bill_number_array   = [111, 222, 333, 444, 555]  

        if not last_bill:
            self.bill_number = random.choice(bill_number_array)
        
        if current_time.hour == 9  and  (current_time - last_bill.created) >= timedelta(hours=3):
            self.bill_number = random.choice(bill_number_array)
        else:
            self.bill_number = last_bill.bill_number + 1

        super().save(force_insert, force_update, using, update_fields)
        
    def __str__(self):
        child = self.bill.children.first()
        return f"#{self.id} {child.name} (bill : {self.bill.id})" if child else f"#{self.id}"







class ProductBillProduct(models.Model):
    product_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)     #TODO: tobe removed
    product_id     = models.PositiveIntegerField()                                  #TODO: tobe removed
    product_object = fields.GenericForeignKey('product_type', 'product_id')         #TODO: tobe removed
    branch_product = models.ForeignKey('base.BranchProduct', on_delete = models.PROTECT, related_name = 'productbill_products_set')
    options        = models.ManyToManyField('base.ProductOptions')
    add_ons        = models.ManyToManyField('base.ProductAddOns')
    quantity       = models.IntegerField()
    unit_price     = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    notes          = models.CharField(max_length = 75, null = True)
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)








class ProductBillReturnedProduct(models.Model):
    product_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE) #TODO: tobe removed
    product_id     = models.PositiveIntegerField()                              #TODO: tobe removed
    product_object = fields.GenericForeignKey('product_type', 'product_id')     #TODO: tobe removed
    branch_product = models.ForeignKey('base.BranchProduct', on_delete = models.PROTECT, related_name = 'productbill_returned_products_set')
    options        = models.ManyToManyField('base.ProductOptions')
    add_ons        = models.ManyToManyField('base.ProductAddOns')
    quantity       = models.IntegerField()
    unit_price     = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True) 
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_bill_returned_products_set')
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)




















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


