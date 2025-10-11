from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
import re

from base import models
from base import libs





class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True, required = True)
    branch           = serializers.PrimaryKeyRelatedField(
        queryset       = models.Branch.objects.all(), 
        required       = True, 
        allow_null     = True,
        error_messages ={
            'invalid': _('Invalid branch ID.'),
            'does_not_exist': _('Selected branch does not exist.'),
            'incorrect_type': _('Branch must be identified by an integer ID.')
        }
    ) 
    staff = serializers.PrimaryKeyRelatedField(
        queryset       = models.Staff.objects.all(), 
        required       = False, 
        error_messages ={
            'invalid': _('Invalid Staff ID.'),
            'does_not_exist': _('Selected Staff does not exist.'),
            'incorrect_type': _('Staff must be identified by an integer ID.')
        }
    ) 
    class Meta: 
        model  = models.User
        fields = [  #is_staff, is_superuser are excluded
            'id',
            'username',
            'phone_number',
            'email',
            'role',
            'is_active',
            'created',
            'updated',
            'created_by',
            'branch',
            'staff',
            'last_login', 
            'last_logout',
            'password',
            'confirm_password',      
        ]
        read_only_fields = [
            'created',
            'updated',
            'last_login',
            'last_logout',
            'created_by',
        ]
        extra_kwargs = {
            'password' : {'write_only' : True, 'required' : True},
            'role' : {'required' : True},
        }


    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            user = request.user
            lower_roles = libs.get_lower_roles(user)
            if instance != user:
                if instance.role not in lower_roles:
                    raise PermissionDenied(_("You Do Not have the permission to access this data"))
                if user.branch and instance.branch != user.branch:
                    raise PermissionDenied(_("You Can not access a user from another branch"))
        data = super().to_representation(instance)
        created_by = instance.created_by
        staff = instance.staff
        branch = instance.branch
        data['created_by'] = created_by.username if created_by else None
        data['created_by_id'] = created_by.id if created_by else None
        data['staff'] = staff.name if staff else None
        data['staff_id'] = staff.id if staff else None
        data['branch'] = branch.name if branch else None
        data['branch_id'] = branch.id if branch else None
        return data


    def validate_username(self, value):
        return value.lower()


    def validate_phone_number(self, value):
        libs.validate_phone_number(value)
        return value
    

    def validate_email(self, value):
        validate_email(value)
        return value


    def validate_role(self, value):
        if value not in libs.roles_power.keys():
            raise ValidationError(_("incorrect role"))
        return value
    

    def validate_password(self, value):
        validate_password(value)
        return value
    

    def validate(self, attrs):
        password          = attrs.get('password')
        confirm_password  = attrs.get('confirm_password')
        if password != confirm_password:
            raise ValidationError(_("Passwords do not match"))
        return attrs
    







    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user                         = self.context['request'].user
        validated_data['password']   = make_password(validated_data['password'])
        validated_data['created_by'] = user
        instance_role                = validated_data['role'] 
        lower_roles                  = libs.get_lower_roles(user)
        

        if instance_role not in lower_roles:
            raise PermissionDenied(_("You can not give a user a role higher or equal to yours"))

        if user.role == 'manager':                          #manager can create users only in his branch
            validated_data['branch'] = user.branch
        ######################
        if instance_role in ['admin', 'owner']:
            validated_data['branch'] = None
        elif validated_data['branch'] == None:
            raise ValidationError(_("Branch can not be null for the given role"))

        return super().create(validated_data)
    
    

        

    def update(self, instance, validated_data):
        user          = self.context['request'].user
        lower_roles   = libs.get_lower_roles(user)
        
        if not validated_data.get('branch'):
            raise ValidationError(_("Branch must have a value"))

        #password encryption
        if validated_data.get('password') : 
            validated_data.pop('confirm_password', None)
            if user.role in ['reception', 'waiter', 'manager']:               #if the role is reception or waiter can only update his password
                if validated_data.get('password'):
                    instance.password = make_password(validated_data['password'])
                    instance.save()
                return instance
        

        if instance == user   and   user.role in ['admin', 'owner']:
            validated_data.pop('branch') 
            validated_data.pop('role') 
            

        #user updates lower_role_users and he is not reception or waiter
        elif instance.role in lower_roles and user.role not in ['reception', 'waiter']:
            if user.role == 'manager': 
                if instance.branch != user.branch:                #ensuring that a manager can not access a user from another branch
                    raise PermissionDenied(_("You Do not have the permission to perform this action"))                             
                validated_data['branch'] = user.branch            #user who does have a branch must create or update a user with the same branch he owns
                          
            if validated_data['role'] not in lower_roles:
                    raise PermissionDenied(_("You can not give a user with a role higher or equal to yours"))
            
            if validated_data['role'] in ['admin', 'owner']:      #ensuring that the admin and owner do not have a branch
                validated_data['branch'] = None
            elif validated_data['branch'] == None:                #ensuring that any other role have a branch
                raise ValidationError(_("Branch can not be null for the given role"))
        
        #user tries to update a higher-role-user
        else:
            raise PermissionDenied(_("You Do not have the permission to perform this action"))
        
        return super().update(instance, validated_data)


