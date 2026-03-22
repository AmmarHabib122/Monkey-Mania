from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.db import transaction

from base import models
from base import libs






'''##############################MaterialSrializers######################################'''

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = [
            'id',
            'name',
            'type',
            'measure_unit',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'created',
            'updated',
            'created_by',
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        created_by = instance.created_by
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        return data
        
    def validate_name(self, value):
        return value.lower()
    
    def validate_type(self, value):
        return value.lower()
    
    def validate_measure_unit(self, value):
        return value.lower()
    

    

    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)













'''##############################BranchMaterialSerializers######################################'''

class BranchMaterialSerializer(serializers.ModelSerializer):
    material  = serializers.PrimaryKeyRelatedField(
        queryset = models.Material.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid material ID.'),
            'does_not_exist': _('You must provide a valid material ID.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    ) 
    branch   = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        required = True,
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.BranchMaterial
        fields = [
            'id',
            'name',
            'material',
            'branch',
            'warning_units',
            'available_units',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'available_units',
            'created',
            'updated',
            'created_by',
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        if request:                   
            if request.user.branch    and    instance.branch != request.user.branch:
                raise PermissionDenied(_("You Can not access a Material from another branch"))
        data = super().to_representation(instance)
        created_by = instance.created_by
        material = instance.material
        branch = instance.branch
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        data['material'] = material.name if material else None
        data['material_id'] = material.id if material else None
        data['branch'] = branch.name if branch else None
        data['branch_id'] = branch.id if branch else None
        return data 




    def validate_warning_units(self, value):
        if value < 0:
            raise ValidationError(_("Warning units can not be negative."))
        return value

    def validate_branch(self, value):
        user = self.context['request'].user
        if user.branch    and    value != user.branch:
            raise PermissionDenied(_("You can not add a material to a differnet branch"))
        return value
    





    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)




'''##############################MaterialTransactionSerializer######################################'''

class MaterialTransactionSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField(read_only=True)
    branch_material = serializers.PrimaryKeyRelatedField(
        queryset = models.BranchMaterial.objects.all(),
        required = True,
        error_messages={
            'does_not_exist': _('You must provide a valid branch material ID.'),
            'incorrect_type': _('Branch material must be identified by an integer ID.')
        }
    )
    branch = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(),
        required = True,
        error_messages={
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    )
    class Meta:
        model = models.MaterialTransaction
        fields = [
            'id',
            'branch_material',
            'branch',
            'quantity',
            'transaction_type',
            'source_type',
            'source_id',
            'source',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'source_type',
            'source_id',
            'source',
            'created',
            'updated',
            'created_by',
        ]

    def to_representation(self, instance):
        data           = super().to_representation(instance)
        created_by     = instance.created_by
        branch_material = instance.branch_material
        branch         = instance.branch
        data['created_by']          = created_by.username if created_by else None
        data['created_by_id']       = created_by.id if created_by else None
        data['branch_material']     = branch_material.name if branch_material else None
        data['branch_material_id']  = branch_material.id if branch_material else None
        data['branch']              = branch.name if branch else None
        data['branch_id']           = branch.id if branch else None
        data['source']              = self.get_source(instance)
        return data

    def get_source(self, obj):
        if obj.source:
            return {'id': obj.source.id, 'type': obj.source_type.model}
        return None

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        return value

    def validate_branch(self, value):
        user = self.context['request'].user
        if user.branch and value != user.branch:
            raise PermissionDenied(_("You can not add a transaction for another branch"))
        return value

    def validate_branch_material(self, value):
        user = self.context['request'].user
        if user.branch and value.branch != user.branch:
            raise PermissionDenied(_("You can not add a transaction for a material from another branch"))
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

