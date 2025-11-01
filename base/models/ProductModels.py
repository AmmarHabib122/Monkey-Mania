from django.db import models








class Product(models.Model):
    layer1      = models.CharField(max_length = 150, db_index=True)
    layer2      = models.CharField(max_length = 150, db_index=True)
    layer3      = models.CharField(max_length = 150)
    created     = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)
    created_by  = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_products_set')

    @property
    def name(self):
        return f"{self.layer2} {self.layer3}"
    
    
    @property
    def sold_units(self):
        return self.branch_products_set.aggregate(total_units=models.Sum('sold_units'))['total_units'] or 0
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['layer2', 'layer3'],
                name   = 'unique_product_name'
            )
        ]


    def __str__(self):
        return self.name












class BranchProduct(models.Model):
    product         = models.ForeignKey('base.Product', on_delete = models.PROTECT, related_name = 'branch_products_set')
    branch          = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'products_set')
    warning_units   = models.IntegerField()
    sold_units      = models.IntegerField(default = 0)
    price           = models.DecimalField(max_digits = 10, decimal_places = 2)
    created         = models.DateTimeField(auto_now_add = True)
    updated         = models.DateTimeField(auto_now = True)
    created_by      = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_products_set')
    

    @property
    def layer1(self):
        return self.product.layer1 
    
    @property
    def layer2(self):
        return self.product.layer2 
    
    @property
    def layer3(self):
        return self.product.layer3 
    
    @property
    def name(self):
        return self.product.name 
    
    @property
    def available_units(self):
        material_consumptions_data          = self.material_consumptions_set.all()
        min_product_material_avalible_units = float('inf')

        for data in material_consumptions_data:
            material_available_units             = data.material.available_units
            product_material_consumption         = data.consumption
            product_material_avalible_units      = material_available_units / (product_material_consumption or 1)
            min_product_material_avalible_units  = min(min_product_material_avalible_units, product_material_avalible_units)

        return min_product_material_avalible_units if min_product_material_avalible_units != float('inf') else 0
    
    @property
    def warning_message(self):
        if self.available_units <= self.warning_units:
            limiting_material = next(
                (data.material for data in self.material_consumptions_set.all()
                if data.material.available_units / (data.consumption or 1) == self.available_units),
                None
            )
            limiting_material = limiting_material.name if limiting_material else "unknown"
            return f"{self.name} has now {self.available_units} units available. Check material {limiting_material}."
        return None
    





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
        return f"#{self.id} {self.branch.name}" if self.branch else f"#{self.id}"
    











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

