
from django.db import models




class CafeProduct(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    old_product          = models.OneToOneField('base.Product', on_delete = models.SET_NULL, related_name = 'cafe_new_product', null=True, blank=True)
    category             = models.ForeignKey('base.CafeProductCategory', on_delete = models.PROTECT, related_name = 'products_set')
    image                = models.CharField(max_length = 255)
    price                = models.DecimalField(max_digits = 10, decimal_places = 2)
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_products_set')

    def __str__(self):
        return f"#{self.id} {self.name}"





class BranchCafeProduct(models.Model):
    product              = models.ForeignKey('base.CafeProduct', on_delete = models.PROTECT, related_name = 'branch_products_set')
    branch               = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_cafe_products_set')
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_cafe_products_set')

    @property
    def name(self):
        return self.product.name

    #TODO: calculate available units based on the reciepe and available materials in the branch
    @property
    def available_units(self):
        return 0

    def __str__(self):
        return f"#{self.id} {self.name} ({self.branch.name})"





class CafeProductSauces(models.Model):
    product              = models.ForeignKey('base.CafeProduct', on_delete = models.PROTECT, related_name = 'sauces_set')
    material             = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'cafe_product_sauces_set')
    consumption          = models.IntegerField
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_product_sauces_set')

    #TODO: calculate available units based on the reciepe and available materials in the branch
    @property
    def available_units(self):
        return 0

    def __str__(self):
        return f"#{self.id} (المنتج = {self.product.name}) - (الصوص = {self.material.name})"





class CafeProductReciepe(models.Model):
    product              = models.ForeignKey('base.CafeProduct', on_delete = models.PROTECT, related_name = 'reciepe_set')
    material             = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'cafe_product_reciepe_set')
    consumption          = models.IntegerField
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_product_reciepes_set')

    def __str__(self):
        return f"#{self.id} {self.name}"


