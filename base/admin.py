from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import transaction

from base import models
from base import libs
from base import serializers


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
admin.site.register(models.Discount)




class CsvImport(forms.Form):
    file = forms.FileField()




class ProductAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_product_upload_csv")]
        return new_urls + urls
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = ['layer1', 'layer2', 'layer3']
            try:
                records = libs.get_csv_file_records(request, required_columns)
                if not records:
                    raise ValidationError(_("CSV file is empty or invalid"))
                with transaction.atomic():
                    for record in records:
                        serializer = serializers.ProductSerializer(data=record, context={'request': request})
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            self.message_user(request, f"CSV error: {first_error}", level=messages.ERROR)
                            return render(request, "admin/upload_csv.html", data)
                        serializer.save() 
                self.message_user(request, "CSV uploaded successfully!", level=messages.SUCCESS)
                return render(request, "admin/base/product/change_list.html", data)
            except ValidationError as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
            except PermissionDenied as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
        return render(request, "admin/upload_csv.html", data)
admin.site.register(models.Product, ProductAdmin)





class MaterialAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_material_upload_csv")]
        return new_urls + urls
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = ['name', 'measure_unit']
            try:
                records = libs.get_csv_file_records(request, required_columns)
                if not records:
                    raise ValidationError(_("CSV file is empty or invalid"))
                with transaction.atomic():
                    for record in records:
                        serializer = serializers.MaterialSerializer(data=record, context={'request': request})
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            self.message_user(request, f"CSV error: {first_error}", level=messages.ERROR)
                            return render(request, "admin/upload_csv.html", data)
                        serializer.save() 
                self.message_user(request, "CSV records created successfully!", level=messages.SUCCESS)
                return render(request, "admin/base/material/change_list.html", data)
            except ValidationError as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
            except PermissionDenied as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
        return render(request, "admin/upload_csv.html", data)
admin.site.register(models.Material, MaterialAdmin)
