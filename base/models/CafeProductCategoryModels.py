from django.db import models



class CafeProductCategory(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    image                = models.CharField(max_length = 255)
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_categories_set')
    
    def __str__(self):
        return f"#{self.id} {self.name}"