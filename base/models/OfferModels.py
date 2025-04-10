from django.db import models
from decimal import Decimal
from django.utils import timezone


class Offer(models.Model):
    name           = models.CharField(max_length = 150, unique = True)
    created        = models.DateTimeField(auto_now_add = True)
    updated        = models.DateTimeField(auto_now = True)
    created_by     = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_offers_set')
    
    @property
    def sold_units(self):
        return self.branch_offers_set.aggregate(total=models.Sum('sold_units'))['total'] or 0
    







class BranchOffer(models.Model):
    offer              = models.ForeignKey('base.Offer', on_delete = models.PROTECT, related_name = 'branch_offers_set')
    branch             = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'offers_set')
    price              = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
    before_sale_price  = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
    sold_units         = models.IntegerField(default = 0)
    expire_date        = models.DateField()
    created            = models.DateTimeField(auto_now_add = True)
    updated            = models.DateTimeField(auto_now = True)
    created_by         = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_offers_set')

    @property
    def name(self):
        return self.offer.name
    
    @property
    def is_active(self):
        return self.expire_date <= timezone.now().date()

    @property
    def before_sale_price(self):
        """Calculate sum of all product prices multiplied by quantities"""
        total = Decimal('0.00')
        for offer_product in self.products_set.all():
            total += offer_product.product.price * offer_product.quantity
        return total.quantize(Decimal('0.00'))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['offer', 'branch'],
                name   = 'unique_branch_offer'
            )
        ]




class BranchOfferProduct(models.Model):
    offer        = models.ForeignKey('base.BranchOffer', on_delete=models.CASCADE, related_name='products_set')
    product      = models.ForeignKey('base.BranchProduct', on_delete=models.CASCADE, related_name = 'offer_products_set')
    quantity     = models.PositiveIntegerField(default=1)  

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['offer', 'product'], name = 'unique_branch_offer_product')
        ]