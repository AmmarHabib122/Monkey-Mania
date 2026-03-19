from django.db import models








class Product(models.Model):
    name        = models.CharField(max_length = 150, unique = True)
    layer1      = models.CharField(max_length = 150) #TODO : remove in future
    layer2      = models.CharField(max_length = 150) #TODO : remove in future
    layer3      = models.CharField(max_length = 150)                #TODO : remove in future
    is_active   = models.BooleanField(default = True)
    category    = models.ForeignKey('base.ProductCategory', on_delete = models.PROTECT, related_name = 'products_set', null = True, blank = True)
    price       = models.DecimalField(max_digits = 10, decimal_places = 2)
    created     = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)
    created_by  = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_products_set')

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['layer2', 'layer3'],
                name   = 'unique_product_name'
            )
        ]


    def __str__(self):
        return f"#{self.id} {self.name}"









class BranchProduct(models.Model):
    product         = models.ForeignKey('base.Product', on_delete = models.PROTECT, related_name = 'branch_products_set')
    branch          = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'products_set')
    price           = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)  #TODO : to be removed in future and use the price from the product model instead
    created         = models.DateTimeField(auto_now_add = True)
    updated         = models.DateTimeField(auto_now = True)
    created_by      = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_products_set')
    
    @property
    def name(self):
        return self.product.name 
    
    #TODO: calculate available units based on the reciepe and available materials in the branch
    @property
    def available_units(self):
        return 0
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['product', 'branch'],
                name   = 'unique_branch_products'
            )
        ]
        
        indexes = [
            models.Index(fields=['branch', 'product']),
        ]
    
    def __str__(self):
        return f"#{self.id} {self.name} ({self.branch.name})"




#TODO : to be reomved in future
class BranchProductMaterial(models.Model):
    product      = models.ForeignKey('base.BranchProduct', on_delete = models.CASCADE, related_name = 'material_consumptions_set')
    material     = models.ForeignKey('base.BranchMaterial', on_delete = models.CASCADE, related_name = 'branch_product_materials_set')
    consumption  = models.DecimalField(max_digits = 14, decimal_places = 6)
    created      = models.DateTimeField(auto_now_add = True)
    updated      = models.DateTimeField(auto_now = True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['product', 'material'],
                name   = 'unique_branch_product_material'
            )
        ]

    def __str__(self):
        return f"#{self.id} {self.product.branch.name} {self.product.name} (material : {self.material.material.name})" if self.product.branch else f"#{self.id}"






class ProductAddOns(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    image                = models.CharField(max_length = 255)
    material             = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'cafe_product_toppings_set')
    consumption          = models.IntegerField
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_product_addons_set')

    
    def __str__(self):
        return f"#{self.id} {self.name}"
    





class ProductCategory(models.Model):
    name                 = models.CharField(max_length = 150, unique = True)
    image                = models.CharField(max_length = 255)
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_product_categories_set')
    
    def __str__(self):
        return f"#{self.id} {self.name}"







class ProductSauces(models.Model):
    product              = models.ForeignKey('base.Product', on_delete = models.PROTECT, related_name = 'sauces_set')
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
    





class ProductReciepe(models.Model):
    product              = models.ForeignKey('base.Product', on_delete = models.PROTECT, related_name = 'reciepe_set')
    material             = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'cafe_product_reciepe_set')
    consumption          = models.IntegerField
    created              = models.DateTimeField(auto_now_add = True)
    updated              = models.DateTimeField(auto_now = True)
    created_by           = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_cafe_product_reciepes_set')

    def __str__(self):
        return f"#{self.id} {self.name}"