from django.db import models

from base import libs





class Bill(models.Model):
    cash             = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    instapay         = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    visa             = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
    hour_price       = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    half_hour_price  = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    time_price       = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    total_price      = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    products_price   = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    is_subscription  = models.BooleanField(default = False) 
    subscription     = models.ForeignKey('base.Subscription', on_delete = models.PROTECT, related_name = 'subscription_bills_set', null = True)
    is_active        = models.BooleanField(default = True)
    children_count   = models.IntegerField(default = 0)
    children         = models.ManyToManyField('base.Child', related_name = "child_bills_set")
    branch           = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_bills_set')
    discount_value   = models.DecimalField(max_digits = 5, decimal_places = 4, default = 0)
    discount_type    = models.CharField(max_length = 50, null = True)
    created_by       = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_bills_set')
    finished_by      = models.ForeignKey('base.User', on_delete = models.PROTECT, null = True, related_name = 'finished_bills_set')
    spent_time       = models.IntegerField(default = 0)
    finished         = models.DateTimeField(null = True)
    created          = models.DateTimeField(auto_now_add = True)
    updated          = models.DateTimeField(auto_now = True)
    #reservations
    #shift


    @property
    def money_unbalance(self):
        return libs.calculate_money_unbalance(self.total_price, self.cash, self.visa, self.instapay)
    


    def update_products_price(self):
        total               = self.product_bills_set.aggregate(total=models.Sum("total_price")).get("total", 0) or 0
        self.products_price = total
        self.save(update_fields=["products_price"])

    def update_total_price(self):
        self.total_price = self.products_price + self.time_price
        self.save(update_fields=["total_price"])
    

