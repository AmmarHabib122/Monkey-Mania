from django.db import models
import datetime

from base import libs


class Bill(models.Model):
    serial                  = models.CharField(max_length = 50, null = True, blank = True, unique = True)
    cash                    = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    instapay                = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    visa                    = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
    hour_price              = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    half_hour_price         = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    time_price              = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    total_price             = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    products_price          = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    is_subscription         = models.BooleanField(default = False) 
    subscription            = models.ForeignKey('base.SubscriptionInstance', on_delete = models.PROTECT, related_name = 'subscription_bills_set', null = True, blank = True)
    is_active               = models.BooleanField(default = True)
    is_calculations_updated = models.BooleanField(default = False) #define whether the bill calculations has been updated by a user
    is_allowed_age          = models.BooleanField(default = True)  #define whether one of the children in the bill must have his parents or not
    children_count          = models.IntegerField(default = 0)
    children                = models.ManyToManyField('base.Child', related_name = "child_bills_set")
    branch                  = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_bills_set')
    discount_value          = models.DecimalField(max_digits = 10, decimal_places = 4, default = 0, blank = True)
    discount_type           = models.CharField(max_length = 50, null = True, blank = True)
    discount                = models.ForeignKey('base.Discount', on_delete = models.PROTECT, related_name = 'discount_bills_set', null = True, blank = True)
    calculations_updated_by = models.ForeignKey('base.User', on_delete = models.PROTECT, null = True, blank = True, related_name = 'calculations_updated_bills_set')
    notes_updated_by        = models.ForeignKey('base.User', on_delete = models.PROTECT, null = True, blank = True, related_name = 'notes_updated_bills_set')
    created_by              = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_bills_set')
    finished_by             = models.ForeignKey('base.User', on_delete = models.PROTECT, null = True, blank = True, related_name = 'finished_bills_set')
    spent_time              = models.IntegerField(default = 0)
    finished                = models.DateTimeField(null = True)
    created                 = models.DateTimeField(auto_now_add = True)
    updated                 = models.DateTimeField(auto_now = True)
    notes                   = models.TextField(null = True, blank = True, default = None)
    #reservations
    #shift

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 1. Save first to let the database handle the auto-increment ID safely
        is_new = self.pk is None
        super().save(force_insert, force_update, using, update_fields)
        
        # 2. Generate the combined 6-digit serial
        if is_new and not self.serial:
            # A. Get the last digit of the current year (e.g., '6' for 2026)
            year_prefix = datetime.datetime.now().strftime('%y')[-1]
            
            # B. Scramble the database ID into a 5-digit number (10000 to 99999)
            # 17389 is our prime key multiplier
            scrambled_suffix = (self.id * 17389) % 90000 + 10000
            
            # C. Combine them into a perfect 6-digit string
            self.serial = f"{scrambled_suffix}{year_prefix}{self.children_count}"
            
            # Save only the serial field back to the database
            update_fields = set(update_fields) if update_fields else set()
            update_fields.add('serial')
            super().save(update_fields=update_fields)

    @property
    def money_unbalance(self):
        return libs.calculate_money_unbalance(self.total_price, self.cash, self.visa, self.instapay)

    @property
    def has_notes(self):
        return bool(self.notes)
    


    def update_products_price(self):
        total               = self.product_bills_set.aggregate(total=models.Sum("total_price")).get("total", 0) or 0
        self.products_price = total
        self.save(update_fields=["products_price", 'updated'])

    def update_total_price(self):
        self.total_price = self.products_price + self.time_price
        self.save(update_fields=["total_price", 'updated'])
    

    def __str__(self):
        child = self.children.first()
        return f"#{self.id} {child.name}" if child else f"#{self.id}"
