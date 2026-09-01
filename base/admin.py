from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
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
admin.site.register(models.OutboundMessage)
admin.site.register(models.WebhookCall)
admin.site.register(models.BillTimePause)
admin.site.register(models.ProductBill)
admin.site.register(models.Discount)
admin.site.register(models.GeneralExpense)
admin.site.register(models.MaterialExpense)
admin.site.register(models.BranchProductMaterial)




class CsvImport(forms.Form):
    file = forms.FileField()




class ProductAdmin(admin.ModelAdmin):
    csv_columns = ['layer1', 'layer2', 'layer3', 'is_active']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_product_upload_csv"),
            path('export_csv/', self.admin_site.admin_view(self.export_csv), name="base_product_export_csv"),
        ]
        return new_urls + urls

    def export_csv(self, request):
        if not self.has_view_or_change_permission(request):
            raise DjangoPermissionDenied

        records = models.Product.objects.order_by('layer1', 'layer2', 'layer3').values(
            'layer1',
            'layer2',
            'layer3',
            'is_active',
        )
        return libs.send_csv_file_response(
            records,
            'products.csv',
            columns=self.csv_columns,
        )
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = self.csv_columns
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
                self.message_user(request, "Products processed using CSV file successfully!", level=messages.SUCCESS)
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
    csv_columns = [
        'layer1',
        'layer2',
        'layer3',
        'branch',
        'warning_units',
        'price',
        'material_consumptions_set',
    ]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_branch_product_upload_csv"),
            path('export_csv/', self.admin_site.admin_view(self.export_csv), name="base_branch_product_export_csv"),
        ]
        return new_urls + urls

    def export_csv(self, request):
        if not self.has_view_or_change_permission(request):
            raise DjangoPermissionDenied

        branch_products = (
            models.BranchProduct.objects
            .select_related('product', 'branch')
            .prefetch_related('material_consumptions_set__material__material')
            .order_by('branch__name', 'product__layer1', 'product__layer2', 'product__layer3', 'id')
        )
        records = []
        for branch_product in branch_products:
            material_consumptions = [
                {
                    'material': material_consumption.material.material.name,
                    'consumption': str(material_consumption.consumption),
                }
                for material_consumption in branch_product.material_consumptions_set.all()
            ]
            records.append({
                'layer1': branch_product.product.layer1,
                'layer2': branch_product.product.layer2,
                'layer3': branch_product.product.layer3,
                'branch': branch_product.branch.name,
                'warning_units': branch_product.warning_units,
                'price': str(branch_product.price),
                'material_consumptions_set': json.dumps(material_consumptions, ensure_ascii=False),
            })

        return libs.send_csv_file_response(
            records,
            'branch_products.csv',
            columns=self.csv_columns,
        )

    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = self.csv_columns
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
                            product = models.Product.objects.get(layer1=layer1, layer2=layer2, layer3=layer3)
                            record['product'] = product.id
                        except models.Product.DoesNotExist:
                            raise ValidationError(f"Product '{layer2} {layer3}' with layer3 equals '{layer3}' does not exist. In Record: {record}")
                        
                        existing_instance = models.BranchProduct.objects.filter(
                            branch_id=record['branch'], 
                            product_id=record['product']
                        ).first()

                        # parse material_consumptions_set from JSON string
                        if 'material_consumptions_set' not in record:
                            raise ValidationError(_("material_consumptions_set must be provided for every record"))
                        try:
                            material_list = json.loads(record['material_consumptions_set'])
                        except Exception as e:
                            raise ValidationError(f"Invalid JSON for material_consumptions_set: {record['material_consumptions_set']}. Error: {e}")

                        if not isinstance(material_list, list):
                            raise ValidationError(f"material_consumptions_set must be a JSON list. In Record: {record}")

                        # replace material names with IDs
                        converted_materials = []
                        for material in material_list:
                            if not isinstance(material, dict) or "material" not in material or "consumption" not in material:
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
                            context={'request': request},
                        )
                        if not serializer.is_valid():
                            errors = serializer.errors
                            first_field, first_messages = next(iter(errors.items()))
                            first_error = first_messages[0]
                            raise ValidationError(f"There is error : {first_error} In Record : {record}")
                        serializer.save()
                self.message_user(request, "Branch products processed using CSV file successfully!", level=messages.SUCCESS)
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
    csv_columns = ['name', 'measure_unit']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_material_upload_csv"),
            path('export_csv/', self.admin_site.admin_view(self.export_csv), name="base_material_export_csv"),
        ]
        return new_urls + urls

    def export_csv(self, request):
        if not self.has_view_or_change_permission(request):
            raise DjangoPermissionDenied

        records = models.Material.objects.order_by('name').values('name', 'measure_unit')
        return libs.send_csv_file_response(
            records,
            'materials.csv',
            columns=self.csv_columns,
        )
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = self.csv_columns
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
    csv_columns = ['material', 'branch', 'available_units']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload_csv/', self.admin_site.admin_view(self.upload_csv), name="base_branch_material_upload_csv"),
            path('export_csv/', self.admin_site.admin_view(self.export_csv), name="base_branch_material_export_csv"),
        ]
        return new_urls + urls

    def export_csv(self, request):
        if not self.has_view_or_change_permission(request):
            raise DjangoPermissionDenied

        branch_materials = (
            models.BranchMaterial.objects
            .select_related('material', 'branch')
            .order_by('branch__name', 'material__name', 'id')
        )
        records = [
            {
                'material': branch_material.material.name,
                'branch': branch_material.branch.name,
                'available_units': str(branch_material.available_units),
            }
            for branch_material in branch_materials
        ]
        return libs.send_csv_file_response(
            records,
            'branch_materials.csv',
            columns=self.csv_columns,
        )
    
    def upload_csv(self, request):
        form = CsvImport()   
        data = {'form': form}
        if request.method == 'POST':
            required_columns = self.csv_columns
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
                self.message_user(request, "Branch materials processed using CSV file successfully!", level=messages.SUCCESS)
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
