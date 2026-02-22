from django.db import models




class Material(models.Model):
    name          = models.CharField(max_length = 155, unique = True)
    measure_unit  = models.CharField(max_length = 30)
    created       = models.DateTimeField(auto_now_add = True)
    updated       = models.DateTimeField(auto_now = True)
    created_by    = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_materials_set')


    # @property
    # def consumption(self):
    #     self.branch_materials_set.aggregate(total_consumption = models.Sum('consumption'))['total_consumption'] or 0

    def __str__(self):
        return f"#{self.id} {self.name} (unit: {self.measure_unit})"






class BranchMaterial(models.Model):
    material         = models.ForeignKey('base.Material', on_delete = models.PROTECT, related_name = 'branch_materials_set')
    branch           = models.ForeignKey('base.Branch', on_delete = models.CASCADE, related_name = 'materials_set')
    available_units  = models.DecimalField(max_digits = 14, decimal_places = 4)
    created          = models.DateTimeField(auto_now_add = True)
    updated          = models.DateTimeField(auto_now = True)
    created_by       = models.ForeignKey('base.User', on_delete = models.PROTECT, related_name = 'created_branch_materials_set')

    @property
    def name(self):
        return self.material.name
    @property
    def measure_unit(self):
        return self.material.measure_unit

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['material', 'branch'],
                name   = 'unique_branch_materials'
            )
        ]
    
    def __str__(self):
        return f"#{self.id} {self.material.name} branch {self.branch.name}"