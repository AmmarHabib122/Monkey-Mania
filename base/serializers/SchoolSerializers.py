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
        
    def validate_name(self, value):
        return value.lower()
    



    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        return super().create(validated_data)
    


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



        