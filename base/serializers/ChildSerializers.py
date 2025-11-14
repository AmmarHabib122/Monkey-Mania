from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import transaction



from base import models
from base import libs






class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumber
        fields = [
            'id',
            'value',
            'created',
            'updated',
        ]
        extra_kwargs = {
            'value': {'validators': []} 
        }
        
    def validate_value(self, value):
        libs.validate_phone_number(value)
        return value



class ChildPhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer()
    class Meta:
        model = models.ChildPhoneNumber
        fields = [
            'id',
            'phone_number',
            'relationship',
        ]
        
    def run_validators(self, value):   
        request = self.context.get('request')
        if not request    or    (request   and   request.method == 'POST'):      
            for validator in self.validators.copy():
                if isinstance(validator, serializers.UniqueTogetherValidator):
                    self.validators.remove(validator)           #manual handling in the child serailizer validate function
        return super().run_validators(value)
    

    def validate_relationship(self, value):
        value = value.lower()
        allowed = ['father', 'mother', 'sibling', 'other']
        if value not in allowed:
            raise ValidationError(_(f"Allowed values: {', '.join(allowed)}."))
        return value



class ChildSerializer(serializers.ModelSerializer):
    child_phone_numbers_set = ChildPhoneNumberSerializer(many = True)
    school  = serializers.PrimaryKeyRelatedField(
        queryset = models.School.objects.all(), 
        required = False,
        allow_null=True,
        error_messages={
            'invalid': _('Invalid school ID.'),
            'does_not_exist': _('You must provide a valid school ID.'),
            'incorrect_type': _('school must be identified by an integer ID.')
        }
    ) 
    class Meta:
        model = models.Child
        fields = [
            'id',
            'name',
            'birth_date',
            'age',
            'notes',
            'address',
            'is_active',
            'is_blocked',
            'special_needs',
            'created',
            'updated',
            'created_by',
            'school',
            'child_phone_numbers_set',
        ]
        read_only_fields = [
            'age',
            'is_active',
            'created',
            'updated',
            'created_by',
        ]

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        created_by = instance.created_by
        data["school_id"] = data.get('school', None)
        data["school"] = instance.school.name if instance.school else None
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        if data.get('child_phone_numbers_set'):
            for dict in data['child_phone_numbers_set']:
                dict.pop('id', None)
                dict.pop('child', None)
                dict['phone_number'] = dict['phone_number']['value']
        data["last_visit_date"]                 = getattr(instance, "last_visit_date", None)
        data["last_bill_id"]                    = getattr(instance, "last_bill_id", None)
        return data
    

    def validate_name(self, value):
        value = value.strip().lower()
        child = models.Child.objects.filter(name__iexact=value).first()
        if child != self.instance:
            raise ValidationError(_("The child name {name} already exists.").format(name = value))
        return value

    def validate_special_needs(self, value):
        user = self.context['request'].user
        if user.role == 'reception':
            raise ValidationError(_("You Do Not have the permission to perform this action."))
        return value
    
    def validate_is_blocked(self, value):
        user = self.context['request'].user
        if user.role == 'reception':
            raise ValidationError(_("You Do Not have the permission to perform this action."))
        return value
    
    def validate_birth_date(self, value):
        if value >= timezone.now().date():
            raise ValidationError(_("Birth-Date can not be in the future."))
        return value

    def validate_child_phone_numbers_set(self, value):
        phone_numbers = [child_phone_number['phone_number']['value'] for child_phone_number in value]
        if len(phone_numbers) != len(set(phone_numbers)):
            raise ValidationError(_("Each Phone-number must be unique per child."))
        return value





    def create(self, validated_data):
        user                           = self.context['request'].user
        validated_data['created_by']   = user
        is_blocked                     = validated_data.pop('is_blocked', None)
        special_needs                  = validated_data.pop('special_needs', None)
        request_phone_numbers          = validated_data.pop('child_phone_numbers_set')
        with transaction.atomic():
            instance            = super().create(validated_data)
            phone_numbers_list  = []

            if request_phone_numbers == []:
                raise ValidationError(_("Child Phone Numbers must be provided."))
            
            for data in request_phone_numbers:
                phone_number, created = models.PhoneNumber.objects.get_or_create(
                    value = data['phone_number']['value'],
                )
                phone_numbers_list.append(
                        models.ChildPhoneNumber(
                        phone_number = phone_number, 
                        relationship = data['relationship'], 
                        child        = instance,
                    ) 
                )
            models.ChildPhoneNumber.objects.bulk_create(phone_numbers_list)
            instance.save()
            return instance




    def update(self, instance, validated_data):
        user                  = self.context['request'].user
        request_phone_numbers = validated_data.pop('child_phone_numbers_set', None)
        
        with transaction.atomic():
            for key, val in validated_data.items():
                setattr(instance, key, val)
            instance.save()

            if request_phone_numbers == [] and user.role == 'reception':
                raise PermissionDenied(_("You Do Not have the permission to delete all Child numbers."))

            if request_phone_numbers is not None:
                old_phone_numbers = [child_phone_number.phone_number for child_phone_number in instance.child_phone_numbers_set.all()]
                instance.child_phone_numbers_set.all().delete()

                if request_phone_numbers != []:
                    new_phone_numbers = [] 
                    for data in request_phone_numbers:
                        phone_number_value = data['phone_number']['value']
                        relationship       = data['relationship']
                        phone_number, created = models.PhoneNumber.objects.get_or_create(
                            value = phone_number_value
                        )
                        new_phone_numbers.append(
                                models.ChildPhoneNumber(
                                phone_number = phone_number,
                                relationship = relationship,
                                child        = instance
                            )
                        )
                    models.ChildPhoneNumber.objects.bulk_create(new_phone_numbers)
                
                for phone_number in old_phone_numbers:
                    if not phone_number.child_phone_number_values_set.exists():
                        phone_number.delete()
            instance.save()
            return instance       



















