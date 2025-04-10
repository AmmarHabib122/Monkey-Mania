from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _

from base import models



class CashierSerializer(serializers.ModelSerializer):
    transaction_type   = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), required = False)
    transaction_id     = serializers.IntegerField(required = False)
    transaction_object = serializers.SerializerMethodField()

    class Meta:
        model = models.Cashier
        fields = [
            'id', 'transaction_type', 'transaction_id', 'transaction_object',
            'branch', 'value', 'created_by', 'created', 'updated'
        ]
        read_only_fields = ['transaction_object', 'created_by', 'created', 'updated']

    def get_transaction_object(self, obj):
        """Retrieve the actual transaction instance."""
        if obj.transaction_object:
            return {
                "id": obj.transaction_object.id,
                "type": obj.transaction_object.__class__.__name__,  # Model name
                "details": str(obj.transaction_object)  # You can modify this as needed
            }
        return None
    
    def validate_value(self, value):
        if value <= 0:
            raise ValidationError(_("Value cannot be negative or equal to zero"))
        return value * -1

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)