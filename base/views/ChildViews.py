from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter

from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']






class CreateChildAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.Child.objects.all()
    serializer_class   = serializers.ChildSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("Child Created successfully")
        return response
    
        
Create_Child = CreateChildAPI.as_view()






class UpdateChildAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.Child.objects.all()
    serializer_class   = serializers.ChildSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("Child Updated successfully")
        return response
Update_Child = UpdateChildAPI.as_view()




class GetChildAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.Child.objects.all()
    serializer_class   = serializers.ChildSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_Child = GetChildAPI.as_view()





class ListNonActiveChildAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Child.objects.filter(is_active = False).order_by('-id')
    pagination_class   = None
    serializer_class   = serializers.ChildSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'child_phone_numbers_set__phone_number__value', 'school__name']
List_NonActiveChild = ListNonActiveChildAPI.as_view()







class ListChildAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.Child.objects.all().order_by('-id')
    serializer_class   = serializers.ChildSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'child_phone_numbers_set__phone_number__value', 'school__name']
    
    def get_queryset(self):
        query     = super().get_queryset()
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
            return libs.send_csv_file_response(serializer.data, "children.csv")
        return super().list(request, *args, **kwargs)
    
List_Child = ListChildAPI.as_view()






