from django.db import IntegrityError, transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from base import models


class BillTimePauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BillTimePause
        fields = [
            'id',
            'bill',
            'reason',
            'finished',
            'created',
            'updated',
            'created_by',
            'finished_by',
            'is_active',
            'duration_in_seconds',
        ]
        read_only_fields = [
            'finished',
            'created',
            'updated',
            'created_by',
            'finished_by',
            'is_active',
            'duration_in_seconds',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = instance.created_by.username
        data['created_by_id'] = instance.created_by_id
        data['finished_by'] = (
            instance.finished_by.username if instance.finished_by else None
        )
        data['finished_by_id'] = instance.finished_by_id
        return data

    def validate_reason(self, value):
        value = value.strip()
        if not value:
            raise ValidationError(_("The reason for time pause cannot be empty"))
        return value

    def validate_bill(self, bill):
        user = self.context['request'].user
        if user.branch and user.branch != bill.branch:
            raise PermissionDenied(_("You do not have the permission to access this bill"))
        if not bill.is_active:
            raise ValidationError(_("You cannot add a time pause to a closed bill"))
        return bill
    

    

    def create(self, validated_data):
        user = self.context['request'].user
        bill = validated_data['bill']

        if user and user.branch and bill.branch != user.branch:
            raise PermissionDenied(_("You can not add a time pause from a different branch"))
        
        if bill.pauses.filter(finished__isnull=True).exists():
            raise ValidationError(_("This bill already has an active time pause"))

        validated_data['created_by'] = user
        validated_data['finished'] = None
        validated_data['finished_by'] = None
        return super().create(validated_data)
    

    def update(self, instance,validated_data):
        user = self.context['request'].user
        
        if user and user.branch and instance.bill.branch != user.branch:
            raise PermissionDenied(_("You can not edit a time pause from a different branch"))

        return super().update(instance, validated_data)
