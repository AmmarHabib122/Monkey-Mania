from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _

from base import models






class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = [
            'id',
            'name',
            'address',
            'notes',
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
    



    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



        