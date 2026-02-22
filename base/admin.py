from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import transaction
from django.urls import reverse
from django.shortcuts import redirect
import json

from base import models
from base import libs
from base import serializers


admin.site.register(models.User)
admin.site.register(models.School)
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
admin.site.register(models.Discount)
admin.site.register(models.GeneralExpense)
admin.site.register(models.MaterialExpense)
admin.site.register(models.BranchProductMaterial)




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
                        # 1. Normalize layers to match the serializer (lowercase & stripped)
                        l1 = str(record.get('layer1', '')).strip().lower()
                        l2 = str(record.get('layer2', '')).strip().lower()
                        l3 = str(record.get('layer3', '')).strip().lower()
                        
                        # 2. Look for an existing Product
                        existing_instance = models.Product.objects.filter(layer1=l1, layer2=l2, layer3=l3).first()

                        # 3. Pass the instance to perform an UPDATE if found
                        serializer = serializers.ProductSerializer(
                            instance=existing_instance,
                            data=record, 
                            context={'request': request}
                        )
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            raise ValidationError(f"There is error : {first_error} In Record : {record}")
                        serializer.save() 
                self.message_user(request, "Products created using CSV file successfully!", level=messages.SUCCESS)
                return redirect(reverse('admin:base_product_changelist'))
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





class BranchProductAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_branch_product_upload_csv")]
        return new_urls + urls
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = ['layer1', 'layer2', 'layer3', 'branch', 'warning_units', 'price', 'material_consumptions_set']
            try:
                records = libs.get_csv_file_records(request, required_columns)
                if not records:
                    raise ValidationError(_("CSV file is empty or invalid"))
                with transaction.atomic():
                    for record in records:
                        # normalize values
                        branch_name = str(record['branch']).strip()
                        layer1 = str(record.pop('layer1')).strip()
                        layer2 = str(record.pop('layer2')).strip()
                        layer3 = str(record.pop('layer3')).strip()

                        try:
                            record['branch'] = models.Branch.objects.get(name=branch_name).id
                        except models.Branch.DoesNotExist:
                            raise ValidationError(f"Branch '{branch_name}' does not exist. In Record: {record}")

                        try:
                            record['product'] = models.Product.objects.get(layer1=layer1, layer2=layer2, layer3=layer3).id
                        except models.Product.DoesNotExist:
                            raise ValidationError(f"Product '{layer2} {layer3}' with layer3 equals '{layer3}' does not exist. In Record: {record}")
                        
                        existing_instance = models.BranchProduct.objects.filter(
                            branch_id=record['branch'], 
                            product_id=record['product']
                        ).first()

                        # parse material_consumptions_set from JSON string
                        try:
                            material_list = json.loads(record['material_consumptions_set'])
                        except Exception as e:
                            raise ValidationError(f"Invalid JSON for material_consumptions_set: {record['material_consumptions_set']}. Error: {e}")

                        # replace material names with IDs
                        converted_materials = []
                        for material in material_list:
                            if "material" not in material or "consumption" not in material:
                                raise ValidationError(f"Each material_consumptions_set item must contain 'material' and 'consumption'. Invalid item: {material}. In Record: {record}")
                            material_name = str(material.get("material")).strip()
                            try:
                                material_obj = models.BranchMaterial.objects.get(material__name=material_name, branch=record['branch'])
                                converted_materials.append({
                                    "material": material_obj.id,
                                    "consumption": material.get("consumption")
                                })
                            except models.BranchMaterial.DoesNotExist:
                                raise ValidationError(f"Material '{material_name}' does not exist. Record: {record}")

                        record['material_consumptions_set'] = converted_materials
                        serializer = serializers.BranchProductSerializer(
                            instance=existing_instance, 
                            data=record, 
                            context={'request': request}
                        )
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            raise ValidationError(f"There is error : {first_error} In Record : {record}")
                        serializer.save() 
                self.message_user(request, "BranchProduct created using CSV file successfully!", level=messages.SUCCESS)
                return redirect(reverse('admin:base_branchproduct_changelist'))
            
            except ValidationError as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
            
            except PermissionDenied as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
            
        return render(request, "admin/upload_csv.html", data)
admin.site.register(models.BranchProduct, BranchProductAdmin)







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
                        # Normalize name to lowercase to match the database/serializer
                        material_name = str(record.get('name', '')).strip().lower()
                        
                        # Look for existing record
                        existing_instance = models.Material.objects.filter(name=material_name).first()

                        # Pass instance if found to perform an UPDATE instead of a CREATE
                        serializer = serializers.MaterialSerializer(
                            instance=existing_instance, 
                            data=record, 
                            context={'request': request}
                        )
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            raise ValidationError(f"There is error : {first_error} In Record : {record}")
                        serializer.save() 
                self.message_user(request, "Material processed using CSV file successfully!", level=messages.SUCCESS)
                return redirect(reverse('admin:base_material_changelist'))
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





class BranchMaterialAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_branch_material_upload_csv")]
        return new_urls + urls
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = ['material', 'branch', 'available_units']
            try:
                records = libs.get_csv_file_records(request, required_columns)
                if not records:
                    raise ValidationError(_("CSV file is empty or invalid"))
                with transaction.atomic():
                    for record in records:
                        branch_name = str(record['branch']).strip()
                        material_name = str(record['material']).strip()
                        try:
                            record['branch'] = models.Branch.objects.get(name=branch_name).id
                        except models.Branch.DoesNotExist:
                            raise ValidationError(f"Branch '{branch_name}' does not exist. In Record : {record}")
                        try:
                            record['material'] = models.Material.objects.get(name=material_name).id
                        except models.Material.DoesNotExist:
                            raise ValidationError(f"Material '{material_name}' does not exist. Record: {record}")
                        
                        # 1. Look for an existing BranchMaterial using the IDs
                        existing_instance = models.BranchMaterial.objects.filter(
                            branch_id=record['branch'], 
                            material_id=record['material']
                        ).first()

                        # 2. Pass the instance to perform an UPDATE if found
                        serializer = serializers.BranchMaterialSerializer(
                            instance=existing_instance,
                            data=record, 
                            context={'request': request}
                        )
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            raise ValidationError(f"There is error : {first_error} In Record : {record}")
                        serializer.save() 
                self.message_user(request, "BranchMaterial created using CSV file successfully!", level=messages.SUCCESS)
                return redirect(reverse('admin:base_branchmaterial_changelist'))
            except ValidationError as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
            except PermissionDenied as e:
                error_text = e.detail[0] if isinstance(e.detail, list) else str(e.detail)
                self.message_user(request, f"CSV error: {error_text}", level=messages.ERROR)
                return render(request, "admin/upload_csv.html", data)
        return render(request, "admin/upload_csv.html", data)
admin.site.register(models.BranchMaterial, BranchMaterialAdmin)