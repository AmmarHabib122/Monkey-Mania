from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from base import serializers
from base import models
from base import permissions
from base import libs




class RoleAccessList:
    role_access_list    = ['owner', 'admin', 'manager', 'reception']






class CreateSchoolAPI(RoleAccessList, generics.CreateAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = _("School Created successfully")
        return response
Create_School = CreateSchoolAPI.as_view()






class UpdateSchoolAPI(RoleAccessList, generics.UpdateAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True if request.method == "PATCH" else False
        response = super().update(request, *args, **kwargs)
        response.data['message'] = _("School Updated successfully")
        return response
Update_School = UpdateSchoolAPI.as_view()




class GetSchoolAPI(RoleAccessList, generics.RetrieveAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    lookup_field       = "pk"
Get_School = GetSchoolAPI.as_view()







class ListSchoolAPI(RoleAccessList, generics.ListAPIView):
    queryset           = models.School.objects.all()
    serializer_class   = serializers.SchoolSerializer
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'address'] 
List_School = ListSchoolAPI.as_view()




class CreateSchoolsFromCsvFile(RoleAccessList, APIView):
    permission_classes = [permissions.Authenticated, permissions.RoleAccess]
    serializer_class   = serializers.SchoolSerializer

    def post(self, request, *args, **kwargs):
        required_columns = ['name', 'address', 'notes']  # adapt as needed
        records = libs.get_csv_file_records(request, required_columns=required_columns)
        if not records:
            raise ValidationError(_("CSV file is empty or invalid"))
        serializer = serializers.SchoolSerializer(data=records, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response({'message' : _("Schools File Created Successfully")}, status=status.HTTP_201_CREATED)
    
BulkCreate_School = CreateSchoolsFromCsvFile.as_view()