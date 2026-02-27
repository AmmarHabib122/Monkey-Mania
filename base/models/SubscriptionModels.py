from django.db import models
from django.utils import timezone



class Subscription(models.Model):
    name                   = models.CharField(max_length = 150, unique = True)
    hours                  = models.DecimalField(max_digits = 5, decimal_places = 2)  #duration in hours
    instance_duration      = models.IntegerField()  
    sold_units             = models.IntegerField(default = 0)
    price                  = models.DecimalField(max_digits = 15, decimal_places = 2)
    is_active              = models.BooleanField(default = True)
    created                = models.DateTimeField(auto_now_add = True)
    updated                = models.DateTimeField(auto_now = True)
    usable_in_branches     = models.ManyToManyField('base.Branch', related_name = 'visit_branch_subscriptions_set')   #what is the allowed branches the child can visit during this subscitption
    creatable_in_branches  = models.ManyToManyField('base.Branch', related_name = 'branch_subscriptions_set')         #which branches can create this subscitption
    created_by             = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_subscriptions_set')
    
    @property
    def is_multi_access(self):
        return self.usable_in_branches.exists()
    
    def __str__(self):
        return f"#{self.id} {self.name}"
    







class SubscriptionInstance(models.Model):
    cash                   = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    instapay               = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0) 
    visa                   = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
    base_hours             = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)  #the hours that the subscription instance was created with
    remaining_hours        = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    expire_date            = models.DateField()
    price                  = models.DecimalField(max_digits = 15, decimal_places = 2)
    subscription           = models.ForeignKey('base.Subscription', on_delete = models.PROTECT,related_name = 'subscription_instances_set')       
    child                  = models.ForeignKey('base.Child', on_delete = models.PROTECT, related_name = 'subscriptions_set')       
    created                = models.DateTimeField(auto_now_add = True)
    updated                = models.DateTimeField(auto_now = True)
    branch                 = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_subscription_instances_set')        
    created_by             = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_subscription_instances_set')

    @property
    def is_active(self):
        return self.expire_date <= timezone.now().date()   and   self.hours > 0
    
    @property
    def name(self):
        return self.subscription.name
    
    @property
    def usable_in_branches(self):
        return self.subscription.usable_in_branches.all() if self.subscription.is_multi_access else self.branch
    
    def __str__(self):
        return f"#{self.id} {self.subscription.name} branch {self.branch.name} for child {self.child.name}"