from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from decimal import Decimal


from base import models



'''##############################GeneralExpenseSerializers######################################'''



class GeneralExpenseSerializer(serializers.ModelSerializer):
    branch  = serializers.PrimaryKeyRelatedField(
        queryset = models.Branch.objects.all(), 
        error_messages={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('You must provide a valid branch ID.'),
            'incorrect_type': _('branch must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.GeneralExpense
        fields = [
            'id',
            'name',
            'unit_price',
            'total_price',
            'quantity',
            'branch',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'unit_price',
            'created',
            'updated',
            'created_by',
        ]
        
    def validate_name(self, value):
        return value.lower()
    
    def validate_total_price(self, value):
        if value < 0: 
            raise ValidationError(_("price can not be negative"))
        return value
    
    def validate_quantity(self, value):
        if value <= 0: 
            raise ValidationError(_("quantity can not be negative or equal to zero"))
        return value
    
    def validate_branch(self, value):
        user = self.context['request'].user
        if user    and    user.branch    and    value != user.branch:
            raise ValidationError(_("You can not add a general expense to a different branch"))
        return value


    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        total_price                    = validated_data.get('total_price')
        quantity                       = validated_data.get('quantity')
        validated_data['unit_price']   = float(total_price) / float(quantity)
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        instance            = super().update(instance, validated_data)
        instance.unit_price = float(instance.total_price) / float(instance.quantity)
        instance.save()
        return instance



        






'''##############################MaterialExpenseSerializers######################################'''

class MaterialExpenseSerializer(serializers.ModelSerializer):
    material  = serializers.PrimaryKeyRelatedField(
        queryset = models.BranchMaterial.objects.all(), 
        error_messages={
            'invalid': _('Invalid material ID.'),
            'does_not_exist': _('You must provide a valid material ID.'),
            'incorrect_type': _('material must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.MaterialExpense
        fields = [
            'id',
            'material',
            'unit_price',
            'total_price',
            'quantity',
            'branch',
            'created',
            'updated',
            'created_by',
        ]
        read_only_fields = [
            'unit_price',
            'branch',
            'created',
            'updated',
            'created_by',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['measure_unit'] = instance.material.measure_unit
        return data
        
    def validate_name(self, value):
        return value.lower()
    
    def validate_total_price(self, value):
        if value < 0: 
            raise ValidationError(_("price can not be negative"))
        return value
    
    def validate_quantity(self, value):
        if value <= 0: 
            raise ValidationError(_("quantity can not be negative or equal to zero"))
        return value

    def validate_material(self, value):
        user = self.context['request'].user
        if user    and    user.branch    and    value.branch != user.branch:
            raise ValidationError(_("You can not add a material expense to a different branch"))
        return value

    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        validated_data['branch']       = validated_data['material'].branch
        total_price                    = validated_data.get('total_price')
        quantity                       = validated_data.get('quantity')
        validated_data['unit_price']   = float(total_price) / float(quantity)
        instance = super().create(validated_data)
        instance.material.available_units += quantity
        instance.material.save()
        instance.save()
        return instance
    


    def update(self, instance, validated_data):
        old_quantity              = instance.quantity
        new_quantity              = validated_data.get('quantity', old_quantity)
        validated_data['branch']  = validated_data['material'].branch if validated_data.get('material') else instance.branch
        instance                  = super().update(instance, validated_data)
        instance.unit_price       = float(instance.total_price) / float(instance.quantity)

        if new_quantity != old_quantity:
            instance.material.available_units += new_quantity - old_quantity
            instance.material.save()
        instance.save()
        return instance



        


