from django.db import models

class Branch(models.Model):
    name                = models.CharField(max_length = 150, unique = True)
    address             = models.CharField(max_length = 255)
    indoor              = models.BooleanField(default=True)
    created             = models.DateTimeField(auto_now_add = True)
    updated             = models.DateTimeField(auto_now = True)
    allowed_age         = models.DecimalField(max_digits = 5, decimal_places = 2)
    manager             = models.ForeignKey('base.User', on_delete = models.PROTECT, null = True, blank = True, related_name = "managed_branches_set")
    created_by          = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branches_set')
    
    #staff delay data        
    delay_allowed_time  = models.IntegerField()
    delay_fine_interval = models.IntegerField()
    delay_fine_value    = models.DecimalField(max_digits = 5, decimal_places = 2)  #number of days

    # products
    # promo_codes
    # offers
    # material
    # subscribtion plan
    def __str__(self):
        return self.name




class HourPrice(models.Model):
    children_count   = models.IntegerField()
    hour_price       = models.DecimalField(max_digits = 20, decimal_places = 2) 
    half_hour_price  = models.DecimalField(max_digits = 20, decimal_places = 2) 
    branch           = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name ='hour_prices_set')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['branch', 'children_count'],
                name   = 'unique_children_count'
            )
        ]
