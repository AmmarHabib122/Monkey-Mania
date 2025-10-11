from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions
from base import libs





'''##############################GeneralExpenseAPIs######################################'''



class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateGeneralExpenseAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.GeneralExpense.objects.all()
    serializer_class   = serializers.GeneralExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("GeneralExpense Created successfully")
        return response
Create_GeneralExpense = CreateGeneralExpenseAPI.as_view()






class UpdateGeneralExpenseAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.GeneralExpense.objects.all()
    serializer_class   = serializers.GeneralExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("GeneralExpense Updated successfully")
        return response
Update_GeneralExpense = UpdateGeneralExpenseAPI.as_view()




class GetGeneralExpenseAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.GeneralExpense.objects.all()
    serializer_class   = serializers.GeneralExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
Get_GeneralExpense = GetGeneralExpenseAPI.as_view()







class ListGeneralExpenseAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.GeneralExpense.objects.all().order_by('-id')
    serializer_class   = serializers.GeneralExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name'] 

    def get_queryset(self):
        branches  = libs.get_branch_ids(self)
        query     = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
    def list(self, request, *args, **kwargs):
        if libs.is_csv_response(request):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return libs.send_csv_file_response(serializer.data, "general_expenses.csv")
        return super().list(request, *args, **kwargs)
    
List_GeneralExpense = ListGeneralExpenseAPI.as_view()


















'''##############################MaterialExpenseAPIs######################################'''


class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager']






class CreateMaterialExpenseAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.MaterialExpense.objects.all()
    serializer_class   = serializers.MaterialExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("MaterialExpense Created successfully")
        return response
Create_MaterialExpense = CreateMaterialExpenseAPI.as_view()






class UpdateMaterialExpenseAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.MaterialExpense.objects.all()
    serializer_class   = serializers.MaterialExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("MaterialExpense Updated successfully")
        return response
Update_MaterialExpense = UpdateMaterialExpenseAPI.as_view()




class GetMaterialExpenseAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.MaterialExpense.objects.all()
    serializer_class   = serializers.MaterialExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def get_object(self):
        obj = super().get_object()
        if self.request.user.branch    and   obj.branch != self.request.user.branch:
            raise PermissionDenied(_("You do not have the permission to access this data"))
        return obj
Get_MaterialExpense = GetMaterialExpenseAPI.as_view()







class ListMaterialExpenseAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.MaterialExpense.objects.all().order_by('-id')
    serializer_class   = serializers.MaterialExpenseSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['material__material__name'] 

    def get_queryset(self):
        branches  = libs.get_branch_ids(self)
        query     = super().get_queryset().filter(branch__in = branches) if branches != ['all'] else super().get_queryset()
        start_date, end_date, is_date_range = libs.get_date_range(self)
        if is_date_range   and   start_date == end_date:
            query = libs.get_all_instances_in_a_day_query(query, start_date)
        elif is_date_range:
            query = libs.get_all_instances_in_a_date_range_query(query, start_date, end_date)
        return query
    
    def list(self, request, *args, **kwargs):
        if libs.is_csv_response(request):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return libs.send_csv_file_response(serializer.data, "material_expenses.csv")
        return super().list(request, *args, **kwargs)
    
List_MaterialExpense = ListMaterialExpenseAPI.as_view()






