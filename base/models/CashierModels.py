from django.db import models
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from base import libs

class Cashier(models.Model):
    transaction_type   = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    transaction_id     = models.PositiveIntegerField()
    transaction_object = fields.GenericForeignKey('transaction_type', 'transaction_id')
    branch             = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'branch_cashier_values_set')
    value              = models.DecimalField(max_digits = 20, decimal_places = 0) 
    created_by         = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cashier_values_set')
    created            = models.DateTimeField(auto_now_add = True)
    updated            = models.DateTimeField(auto_now = True)

   