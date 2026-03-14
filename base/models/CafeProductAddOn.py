from django.db import models




class CafeProductAddOn(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    image                = models.CharField(max_length = 255)
    material             = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'cafe_product_toppings_set')
    consumption          = models.IntegerField
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_product_addons_set')

    
    def __str__(self):
        return f"#{self.id} {self.name}"