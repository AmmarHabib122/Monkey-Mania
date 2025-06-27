from django.contrib import admin
from base import models


admin.site.register(models.User)
admin.site.register(models.Branch)
admin.site.register(models.HourPrice)
admin.site.register(models.Child)
admin.site.register(models.ChildPhoneNumber)
admin.site.register(models.PhoneNumber)
admin.site.register(models.Image)
admin.site.register(models.Staff)
admin.site.register(models.StaffWithdraw)
admin.site.register(models.StaffFine)
admin.site.register(models.StaffSalary)
admin.site.register(models.Bill)
admin.site.register(models.ProductBill)
admin.site.register(models.ProductBillProduct)
admin.site.register(models.Product)
admin.site.register(models.BranchProduct)
admin.site.register(models.Material)
admin.site.register(models.BranchMaterial)
admin.site.register(models.Discount)
