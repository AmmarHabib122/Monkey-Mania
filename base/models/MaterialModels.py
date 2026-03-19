from django.db import models




class Material(models.Model):
    MATERIAL_TYPES = [
        ('kids', 'kids'),
        ('cafe', 'cafe'),
    ]

    name          = models.CharField(max_length = 155, unique = True)
    type          = models.CharField(max_length = 50, choices=MATERIAL_TYPES, default='cafe')
    created       = models.DateTimeField(auto_now_add = True)
    updated       = models.DateTimeField(auto_now = True)
    created_by    = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_materials_set')


    def __str__(self):
        return f"#{self.id} {self.name} (unit: {self.measure_unit})"




class BranchMaterial(models.Model):
    material         = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'branch_materials_set')
    branch           = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'materials_set')
    warning_units    = models.IntegerField()
    created          = models.DateTimeField(auto_now_add = True)
    updated          = models.DateTimeField(auto_now = True)
    created_by       = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_materials_set')

    @property
    def name(self):
        return self.material.name


    #TODO: calculate available units based on the transactions of this material in this branch (purchases, usages in cafe products, etc.)
    @property
    def available_units(self):
        return 0

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['material', 'branch'],
                name   = 'unique_branch_materials'
            )
        ]

    def __str__(self):
        return f"#{self.id} {self.material.name} ({self.branch.name})"



class MaterialTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('stock_out', 'stock_out'),
        ('stock_in', 'stock_in'),
    ]
    material         = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'transactions_set')
    branch           = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'material_transactions_set')
    quantity         = models.IntegerField()
    transaction_type = models.CharField(max_length = 50, choices=TRANSACTION_TYPES)
    created          = models.DateTimeField(auto_now_add = True)
    updated          = models.DateTimeField(auto_now = True)
    created_by       = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_material_transactions_set')
