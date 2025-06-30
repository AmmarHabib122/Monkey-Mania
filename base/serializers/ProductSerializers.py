from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.db import transaction

from base import models
from base import libs






'''##############################ProductSrializers######################################'''

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'id',
            'layer1',
            'layer2',
            'layer3',
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]

    def validate_layer1(self, value):
        return value.lower()
    
    def validate_layer2(self, value):
        return value.lower()
    
    def validate_layer3(self, value):
        return value.lower()
    



    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)





'''##############################BranchProductMaterialSrializers######################################'''

class BranchProductMaterialSerializer(serializers.ModelSerializer):
    material  = serializers.PrimaryKeyRelatedField(
        queryset = models.BranchMaterial.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid material ID.'),
            'does_not_exist': _('You must provide a valid material ID.'),
            'incorrect_type': _('Material must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.BranchProductMaterial
        fields = [
            'id',
            # 'product',
            'material',
            'consumption',
        ]

    def validate_consumption(self, value):
        if value < 0: 
            raise ValidationError(_("consumption can not be negative."))
        return value
    
    def validate_material(self, value):
        request = self.context.get('request')
        if request:                   
            if request.user.branch    and    value.branch != request.user.branch:
                raise PermissionDenied(_("You Can not access a material from another branch"))  
        return value
        















'''##############################BranchProductSerializers######################################'''

class BranchProductSerializer(serializers.ModelSerializer):
    material_consumptions_set = BranchProductMaterialSerializer(many = True)
    product      = serializers.PrimaryKeyRelatedField(
        queryset = models.Product.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid product ID.'),
            'does_not_exist': _('You must provide a valid product ID.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    ) 
    branch  = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.BranchProduct
        fields = [
            'id',
            'layer1',
            'layer2',
            'layer3',
            'name',
            'product',
            'branch',
            'warning_units',
            'available_units',
            'warning_message',
            'sold_units',
            'price',
            'material_consumptions_set',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'layer1',
            'layer2',
            'layer3',
            'name',
            'available_units',
            'warning_message',
            'sold_units',
            'created',
            'updated',
            'created_by',
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:                   
            if request.user.branch    and    instance.branch != request.user.branch:
                raise PermissionDenied(_("You Can not access a Product from another branch"))
        data = super().to_representation(instance)
        data['material_consumptions_set'] = BranchProductMaterialSerializer(instance.material_consumptions_set.all(), many = True).data
        for material_data in data['material_consumptions_set']:
            branch_material = models.BranchProductMaterial.objects.get(id = material_data['id'])
            material_data['material']     = branch_material.material.name
            material_data['measure_unit'] = branch_material.material.measure_unit
        return data




    def validate_warning_units(self, value):
        if value < 0: 
            raise ValidationError(_("Warning Units can not be negative."))
        return value
    
    def validate_price(self, value):
        if value <= 0: 
            raise ValidationError(_("Price can not be negative or equal to zero."))
        return value
    
    def validate_branch(self, value):
        user   = self.context['request'].user
        if    user.branch    and    value != user.branch:
            raise PermissionDenied(_("You can not add a product to this branch"))
        return value
    
    def validate_material_consumptions_set(self, value):
        if value == []:
            raise ValidationError(_("Materials must be provided."))
        else:
            material_ids = []
            for data in value:
                material_id = data['material'].id
                if material_id in material_ids:
                    raise ValidationError(_("You tried to add the same material more than once"))
                else:
                    material_ids.append(material_id)
        return value
    
    def validate(self, attrs):
        materials = attrs.get('material_consumptions_set')
        branch    = attrs.get('branch')
        if materials and branch:
            for data in materials:
                # material = models.BranchMaterial.objects.filter(id = data['material'])
                if data['material'].branch != branch:
                    raise ValidationError(_('This material is not valid for this branch'))
        return super().validate(attrs)






    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        request_materials              = validated_data.pop('material_consumptions_set', [])

        
        
        with transaction.atomic():
            instance        = super().create(validated_data)
            materials_list  = [] 

            
            for data in request_materials:
                materials_list.append(
                        models.BranchProductMaterial(
                        product       = instance, 
                        material      = data['material'], 
                        consumption   = data['consumption'],
                    ) 
                )
            models.BranchProductMaterial.objects.bulk_create(materials_list)
            instance.save()
            return instance
    





    def update(self, instance, validated_data):
        user                           = self.context['request'].user
        request_materials              = validated_data.pop('material_consumptions_set', None)

        
            
        with transaction.atomic():
            instance        = super().update(instance, validated_data)
            materials_list  = [] 

            if request_materials is not None:
                instance.material_consumptions_set.all().delete()
                for data in request_materials:
                    materials_list.append(
                            models.BranchProductMaterial(
                            product       = instance, 
                            material      = data['material'], 
                            consumption   = data['consumption'],
                        ) 
                    )
                models.BranchProductMaterial.objects.bulk_create(materials_list)
            instance.save()
            return instance
    




