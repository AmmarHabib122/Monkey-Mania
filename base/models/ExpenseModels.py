from django.db import models



class GeneralExpense(models.Model):
    name         = models.CharField(max_length = 150)
    unit_price   = models.DecimalField(max_digits = 14, decimal_places = 2)
    total_price  = models.DecimalField(max_digits = 16, decimal_places = 2)
    quantity     = models.IntegerField(default = 1)
    branch       = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_general_expenses_set')
    created      = models.DateTimeField(auto_now_add = True)
    updated      = models.DateTimeField(auto_now = True)
    created_by   = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_general_expenses_set')
    
    def __str__(self):
        return f"#{self.id} {self.name} {self.quantity} items  branch {self.branch.name}"
    
    



class MaterialExpense(models.Model):
    material     = models.ForeignKey('base.BranchMaterial', on_delete = models.PROTECT, related_name = 'material_expenses_set')
    unit_price   = models.DecimalField(max_digits = 14, decimal_places = 2)
    total_price  = models.DecimalField(max_digits = 16, decimal_places = 2)
    quantity     = models.IntegerField(default = 1)
    branch       = models.ForeignKey('base.Branch', on_delete = models.PROTECT, related_name = 'branch_material_expenses_set')
    created      = models.DateTimeField(auto_now_add = True)
    updated      = models.DateTimeField(auto_now = True)
    created_by   = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_material_expenses_set')
    
    def __str__(self):
        return f"#{self.id} {self.material.name} {self.quantity} items  branch {self.branch.name}"
    
    