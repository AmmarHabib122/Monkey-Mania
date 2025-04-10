from django.db import models
from django.utils import timezone


class Discount(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    value                = models.DecimalField(max_digits = 8, decimal_places = 3)
    type                 = models.CharField(max_length = 20)
    expire_date          = models.DateField()
    branches             = models.ManyToManyField('base.Branch', related_name = 'branch_discounts_set')
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_discounts_set')

    @property
    def is_active(self):
        return self.expire_date < timezone.now().date()
    
    
