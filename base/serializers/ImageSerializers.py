from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _

from base import models
from base import libs





class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = [
            'id',
            'value', 
        ]

    def validate_value(self, value):
        max_size = 3 * 1024 * 1024
        if value.size > max_size:
            raise ValidationError(f"Image file is too large! Max size allowed: {max_size / (1024 * 1024)}MB")
        return value

