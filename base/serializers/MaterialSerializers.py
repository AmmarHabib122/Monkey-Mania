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
            'measure_unit',
            # 'consumption',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            # 'consumption',
            'created',
            'updated',
            'created_by',
        ]

    def validate_name(self, value):
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
            'measure_unit',
            'material',
            'branch',
            'available_units',
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
        request = self.context.get('request')
        if request:                   
            if request.user.branch    and    instance.branch != request.user.branch:
                raise PermissionDenied(_("You Can not access a Material from another branch"))
        return super().to_representation(instance)




    def validate_available_units(self, value):
        if value < 0: 
            raise ValidationError(_("Quantity can not be negative."))
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
    
