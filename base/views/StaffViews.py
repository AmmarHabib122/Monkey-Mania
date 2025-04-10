from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from django.db import transaction
import hashlib

from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']




class CreateStaffAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Staff.objects.all()
    serializer_class   = serializers.StaffSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            images             = request.FILES.getlist('images', None)
            images             = list(images) if not isinstance(images, list) else images
            response           = super().create(request, *args, **kwargs)
            staff              = models.Staff.objects.get(id = response.data['id'])
            new_hashes         = set()

            for image in images:

                image.file.seek(0)
                hasher = hashlib.sha256()
                for chunk in image.chunks():
                    hasher.update(chunk) 
                image_hash = hasher.hexdigest()
                image.file.seek(0)

                existing_image = models.Image.objects.filter(hash = image_hash)
                if existing_image.exists():
                    if image_hash not in new_hashes:
                        staff.images.add(existing_image.first())
                else:
                    data             = {"value" : image}
                    image_serializer = serializers.ImageSerializer(data = data)
                    image_serializer.is_valid(raise_exception = True)
                    image_serializer.save()
                    staff.images.add(image_serializer.instance)

                new_hashes.add(image_hash)

            response.data = serializers.StaffSerializer(staff).data
            response.data['message'] = _("Staff Created successfully")
            return response
Create_Staff = CreateStaffAPI.as_view()






class UpdateStaffAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Staff.objects.all()
    serializer_class   = serializers.StaffSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        
        with transaction.atomic():
            images               = request.FILES.getlist('images', None)
            images               = list(images) if not isinstance(images, list) else images
            response             = super().update(request, *args, **kwargs)
            staff                = models.Staff.objects.get(id = response.data['id'])
            current_images       = list(staff.images.all())
            current_hashes       = {image.hash for image in current_images}
            new_hashes           = set()
 
            if images == []:
                staff.images.clear()

            elif images is not None:
                for image in images:
                    image.file.seek(0)
                    hasher = hashlib.sha256()
                    for chunk in image.chunks():
                        hasher.update(chunk) 
                    image_hash = hasher.hexdigest()
                    image.file.seek(0)

                    existing_image = models.Image.objects.filter(hash = image_hash)
                    if existing_image.exists():
                        if image_hash not in current_hashes and image_hash not in new_hashes:         #prevent duplicate images
                            staff.images.add(existing_image.first())
                    else:
                        data             = {"value" : image}
                        image_serializer = serializers.ImageSerializer(data = data)
                        image_serializer.is_valid(raise_exception = True)
                        image_serializer.save()
                        staff.images.add(image_serializer.instance)

                    new_hashes.add(image_hash)

                hashes_to_remove = current_hashes - new_hashes
                for image in current_images:
                    if image.hash in hashes_to_remove:
                        staff.images.remove(image)
                        if not image.staff_images_set.exists():  
                            image.delete()

        response.data = serializers.StaffSerializer(staff).data
        response.data['message'] = _("Staff Updated successfully")
        return response
Update_Staff = UpdateStaffAPI.as_view()




class GetStaffAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Staff.objects.all()
    serializer_class   = serializers.StaffSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
    
Get_Staff = GetStaffAPI.as_view()







class ListStaffAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Staff.objects.all()
    serializer_class   = serializers.StaffSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'phone_number'] 

    def get_queryset(self):
        branch = libs.get_one_branch_id(self)
        query  = models.Staff.objects.filter(branch = branch)
        return query
    
List_Staff = ListStaffAPI.as_view()













'''##############################StaffWithdrawAPIs######################################'''



class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateStaffWithdrawAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.StaffWithdraw.objects.all()
    serializer_class   = serializers.StaffWithdrawSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("StaffWithdraw Created successfully")
        return response
Create_StaffWithdraw = CreateStaffWithdrawAPI.as_view()






class UpdateStaffWithdrawAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.StaffWithdraw.objects.all()
    serializer_class   = serializers.StaffWithdrawSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("StaffWithdraw Updated successfully")
        return response
Update_StaffWithdraw = UpdateStaffWithdrawAPI.as_view()




class GetStaffWithdrawAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.StaffWithdraw.objects.all()
    serializer_class   = serializers.StaffWithdrawSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
Get_StaffWithdraw = GetStaffWithdrawAPI.as_view()







class ListStaffWithdrawAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.StaffWithdraw.objects.all()
    serializer_class   = serializers.StaffWithdrawSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['staff__name', 'staff__phone_number'] 

    def get_queryset(self):
        branch   = libs.get_one_branch_id(self)
        query    = super().get_queryset().filter(branch=branch)
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
List_StaffWithdraw = ListStaffWithdrawAPI.as_view()














'''##############################StaffFinesAPIs######################################'''



class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateStaffFineAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.StaffFine.objects.all()
    serializer_class   = serializers.StaffFineSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("StaffFine Created successfully")
        return response
Create_StaffFine = CreateStaffFineAPI.as_view()






class UpdateStaffFineAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.StaffFine.objects.all()
    serializer_class   = serializers.StaffFineSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("StaffFine Updated successfully")
        return response
Update_StaffFine = UpdateStaffFineAPI.as_view()




class GetStaffFineAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.StaffFine.objects.all()
    serializer_class   = serializers.StaffFineSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
Get_StaffFine = GetStaffFineAPI.as_view()







class ListStaffFineAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.StaffFine.objects.all()
    serializer_class   = serializers.StaffFineSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['staff__name', 'staff__phone_number', 'reason'] 

    def get_queryset(self):
        branch   = libs.get_one_branch_id(self)
        query    = super().get_queryset().filter(branch=branch)
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
List_StaffFine = ListStaffFineAPI.as_view()







'''##############################StaffSalarysAPIs######################################'''



class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateStaffSalaryAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.StaffSalary.objects.all()
    serializer_class   = serializers.StaffSalarySerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("StaffSalary Created successfully")
        return response
Create_StaffSalary = CreateStaffSalaryAPI.as_view()






class UpdateStaffSalaryAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.StaffSalary.objects.all()
    serializer_class   = serializers.StaffSalarySerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("StaffSalary Updated successfully")
        return response
Update_StaffSalary = UpdateStaffSalaryAPI.as_view()




class GetStaffSalaryAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.StaffSalary.objects.all()
    serializer_class   = serializers.StaffSalarySerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
    
Get_StaffSalary = GetStaffSalaryAPI.as_view()







class ListStaffSalaryAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.StaffSalary.objects.all()
    serializer_class   = serializers.StaffSalarySerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['staff__name', 'staff__phone_number'] 

    def get_queryset(self):
        branch   = libs.get_one_branch_id(self)
        query    = super().get_queryset().filter(branch=branch)
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
List_StaffSalary = ListStaffSalaryAPI.as_view()